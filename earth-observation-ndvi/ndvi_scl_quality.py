
"""Screen Sentinel-2 NDVI pixels using the Scene Classification Layer."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.vrt import WarpedVRT

FOLDER = Path(__file__).resolve().parent
NDVI_FILE = FOLDER / "sentinel_ndvi.tif"

SCL_URL = (
    "https://sentinel-cogs.s3.us-west-2.amazonaws.com/"
    "sentinel-s2-l2a-cogs/33/S/VB/2021/2/"
    "S2B_33SVB_20210221_0_L2A/SCL.tif"
)

SCL_NAMES = {
    0: "No data",
    1: "Saturated/defective",
    2: "Dark pixels",
    3: "Cloud shadows",
    4: "Vegetation",
    5: "Not vegetated",
    6: "Water",
    7: "Unclassified",
    8: "Medium-prob. cloud",
    9: "High-prob. cloud",
    10: "Thin cirrus",
    11: "Snow/ice",
}

# For this exercise, retain classified land pixels only.
KEEP_CLASSES = [4, 5]


def distribution(values):
    counts = [
        np.count_nonzero(values < 0.2),
        np.count_nonzero((values >= 0.2) & (values < 0.5)),
        np.count_nonzero(values >= 0.5),
    ]
    return [100 * n / values.size for n in counts]


def main():
    # 1. Read our existing NDVI GeoTIFF.
    with rasterio.open(NDVI_FILE) as src:
        ndvi = np.asarray(
            src.read(1, masked=True).filled(np.nan),
            dtype=np.float32,
        )
        profile = src.profile.copy()
        crs = src.crs
        transform = src.transform
        width, height = src.width, src.height

    # 2. Read remote SCL and align it to our NDVI grid.
    print("Reading remote SCL layer...")

    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
        with rasterio.open(SCL_URL) as src:
            print("Original SCL pixel size:", src.res)

            with WarpedVRT(
                src,
                crs=crs,
                transform=transform,
                width=width,
                height=height,
                resampling=Resampling.nearest,
            ) as aligned:
                scl = aligned.read(
                    1, masked=True
                ).filled(0).astype(np.uint8)

    print("NDVI pixel size:", (abs(transform.a), abs(transform.e)))

    # 3. Examine classifications in this image subset.
    print("\n=== SCL class counts ===")

    classes, counts = np.unique(scl, return_counts=True)

    for code, count in zip(classes, counts):
        name = SCL_NAMES.get(int(code), "Other")
        print(f"{int(code):2d} {name:<22} {count:,} pixels")

    # 4. Create the quality mask.
    valid = np.isfinite(ndvi) & (ndvi >= -1) & (ndvi <= 1)
    retained = valid & np.isin(scl, KEEP_CLASSES)

    before = ndvi[valid]
    after = ndvi[retained]

    if before.size == 0 or after.size == 0:
        raise ValueError("No valid pixels in one comparison group.")

    print("\n=== Before vs after SCL screening ===")

    print("Original valid pixels:", before.size)
    print("Retained land pixels:", after.size)
    print(
        "Retained share:",
        f"{100 * after.size / before.size:.1f}%"
    )

    print(f"Mean NDVI: {before.mean():.3f} -> {after.mean():.3f}")
    print(
        f"Median NDVI: {np.median(before):.3f}"
        f" -> {np.median(after):.3f}"
    )

    labels = ["Low (<0.2)", "Moderate (0.2-0.5)", "High (>=0.5)"]

    for label, b, a in zip(
        labels, distribution(before), distribution(after)
    ):
        print(f"{label:<22} {b:5.1f}% -> {a:5.1f}%")

    print("Each percentage uses its own valid-pixel denominator.")

    # 5. Save a geographically referenced screened NDVI raster.
    output_tif = FOLDER / "sentinel_ndvi_scl_screened.tif"

    profile.update(
        dtype="float32",
        count=1,
        nodata=-9999.0,
        compress="deflate",
    )

    with rasterio.open(output_tif, "w", **profile) as dst:
        dst.write(
            np.where(retained, ndvi, -9999.0).astype("float32"),
            1,
        )

    # 6. Compare the same area before and after screening.
    fig, axes = plt.subplots(
        1, 2, figsize=(11, 5), constrained_layout=True
    )

    for ax, values, title in [
        (
            axes[0],
            np.where(valid, ndvi, np.nan),
            "Before SCL screening",
        ),
        (
            axes[1],
            np.where(retained, ndvi, np.nan),
            "After SCL screening",
        ),
    ]:
        image = ax.imshow(
            values, cmap="RdYlGn", vmin=0, vmax=0.8
        )
        ax.set_title(title)
        ax.set_xlabel("Pixel column")
        ax.set_ylabel("Pixel row")

    fig.colorbar(image, ax=axes, label="NDVI", shrink=0.75)

    output_png = FOLDER / "ndvi_scl_before_after.png"
    fig.savefig(output_png, dpi=160)
    plt.close(fig)

    print("\nSaved:", output_tif.name)
    print("Saved:", output_png.name)
    print("SCL classifications are not ground-truth labels.")


if __name__ == "__main__":
    main()
