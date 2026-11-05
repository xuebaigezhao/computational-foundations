
"""Find a clearer Sentinel-2 scene over our existing NDVI footprint."""
from pathlib import Path
import json
from urllib.request import Request, urlopen

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.vrt import WarpedVRT
from rasterio.warp import transform_bounds

ROOT = Path(__file__).resolve().parent
API = "https://earth-search.aws.element84.com/v1/search"
DATES = "2021-02-01T00:00:00Z/2021-04-30T23:59:59Z"
OLD_SCENE = "S2B_33SVB_20210221_0_L2A"
KEEP_SCL = [4, 5]  # Vegetation + not vegetated land


def main():
    # Use our existing GeoTIFF to define the EXACT study area.
    with rasterio.open(ROOT / "sentinel_ndvi.tif") as ds:
        ndvi = ds.read(1, masked=True).filled(np.nan)
        valid = np.isfinite(ndvi) & (ndvi >= -1) & (ndvi <= 1)
        grid = dict(crs=ds.crs, transform=ds.transform,
                    width=ds.width, height=ds.height)
        bbox = transform_bounds(ds.crs, "EPSG:4326", *ds.bounds)

    if not valid.any():
        raise ValueError("No valid NDVI pixels in existing raster")

    # Search a public satellite imagery catalogue.
    payload = {
        "collections": ["sentinel-2-l2a"],
        "bbox": list(bbox),
        "datetime": DATES,
        "limit": 100,
    }
    request = Request(
        API,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    print("Searching Earth Search over the same study area...")

    try:
        with urlopen(request, timeout=45) as response:
            items = json.load(response)["features"]
    except Exception as error:
        print("Catalogue search failed; check network:", error)
        return

    # Keep the same tile and exclude our original cloudy scene.
    items = [
        item for item in items
        if "_33SVB_" in item["id"]
        and item["id"] != OLD_SCENE
        and all(
            k in item.get("assets", {})
            for k in ("scl", "red", "nir")
        )
    ]

    items.sort(
        key=lambda item: float(
            item["properties"].get("eo:cloud_cover")
            if item["properties"].get("eo:cloud_cover") is not None
            else 100
        )
    )

    if not items:
        print("No suitable scenes found. Try extending DATES.")
        return

    print("Same-tile candidates returned:", len(items))
    print("Checking SCL for the 5 best scene-level cloud scores...")

    ranked = []

    for item in items[:5]:
        cloud_cover = item["properties"].get("eo:cloud_cover")

        try:
            # Align 20 m SCL to our existing 10 m NDVI grid.
            with rasterio.Env(
                GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"
            ):
                with rasterio.open(
                    item["assets"]["scl"]["href"]
                ) as scl_src:
                    with WarpedVRT(
                        scl_src,
                        **grid,
                        resampling=Resampling.nearest,
                    ) as aligned:
                        scl = aligned.read(
                            1, masked=True
                        ).filled(0)

            local_keep = valid & np.isin(scl, KEEP_SCL)
            percent = 100 * local_keep.sum() / valid.sum()

            ranked.append((percent, item))

            print(
                f"{item['id']}: scene cloud {cloud_cover}%, "
                f"local SCL 4/5 retained {percent:.1f}%"
            )

        except Exception as error:
            print(
                f"{item['id']}: unable to read SCL: {error}"
            )

    if not ranked:
        print("No candidate SCL could be read.")
        return

    # Select the best of the scenes we actually checked.
    percent, chosen = max(
        ranked, key=lambda pair: pair[0]
    )

    selection = {
        "id": chosen["id"],
        "datetime": chosen["properties"].get("datetime"),
        "local_retained_percent": round(percent, 2),
        "assets": {
            key: chosen["assets"][key]["href"]
            for key in ("red", "nir", "scl")
        },
    }

    path = ROOT / "selected_sentinel_scene.json"
    path.write_text(
        json.dumps(selection, indent=2),
        encoding="utf-8",
    )

    print("\nBEST TESTED SCENE:", selection["id"])
    print(
        f"Local retained fraction: {percent:.1f}% "
        "(original: 9.3%)"
    )
    print("Saved:", path.name)
    print(
        "Important: different acquisition dates "
        "can differ seasonally."
    )


if __name__ == "__main__":
    main()
