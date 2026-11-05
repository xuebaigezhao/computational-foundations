"""Compare land-masked Sentinel-2 NDVI over an identical grid.

Requires existing sentinel_ndvi_scl_screened.tif and selected_sentinel_scene.json.
Run from any working directory; source data stay unchanged.
"""
from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.vrt import WarpedVRT

ROOT = Path(__file__).resolve().parent
OLD_TIF = ROOT / "sentinel_ndvi_scl_screened.tif"
SELECTION = ROOT / "selected_sentinel_scene.json"
KEEP_SCL = (4, 5)
NODATA = -9999.0


def read_aligned(url, grid, resampling):
    """Read a remote COG, aligned to the original NDVI raster grid."""
    with rasterio.open(url) as source:
        with WarpedVRT(source, **grid, resampling=resampling) as aligned:
            return aligned.read(1, masked=True).astype("float32").filled(np.nan)


def report(label, values):
    valid_values = values[np.isfinite(values)]
    if valid_values.size == 0:
        print(f"{label}: no valid pixels")
        return
    print(
        f"{label}: n={valid_values.size:,}, "
        f"mean={valid_values.mean():.3f}, "
        f"median={np.median(valid_values):.3f}, "
        f"high NDVI >=0.5: {np.mean(valid_values >= 0.5) * 100:.1f}%"
    )


def main():
    selected = json.loads(SELECTION.read_text(encoding="utf-8"))
    assets = selected["assets"]

    with rasterio.open(OLD_TIF) as old_src:
        old = old_src.read(1, masked=True).astype("float32").filled(np.nan)
        profile = old_src.profile.copy()
        grid = {
            "crs": old_src.crs,
            "transform": old_src.transform,
            "width": old_src.width,
            "height": old_src.height,
        }

    print("Selected scene:", selected["id"])
    print("Acquisition date:", selected["datetime"])
    print("Reading remote Red, NIR and SCL over the same footprint...")

    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
        red = read_aligned(assets["red"], grid, Resampling.bilinear)
        nir = read_aligned(assets["nir"], grid, Resampling.bilinear)
        scl = read_aligned(assets["scl"], grid, Resampling.nearest)

    # Both reflectance bands use the same scale, which cancels in NDVI.
    # Exclude nodata and zero denominators, then retain only SCL classes 4/5.
    denominator = nir + red
    spectral_valid = (
        np.isfinite(red) & np.isfinite(nir) & (denominator > 0)
    )
    scl_keep = np.isin(scl, KEEP_SCL)
    usable = spectral_valid & scl_keep

    new = np.full(red.shape, np.nan, dtype="float32")
    with np.errstate(divide="ignore", invalid="ignore"):
        np.divide(nir - red, denominator, out=new, where=usable)
    new[(new < -1) | (new > 1)] = np.nan

    old_ok = np.isfinite(old)
    new_ok = np.isfinite(new)
    common = old_ok & new_ok

    print("\n=== Usable coverage ===")
    print(f"Old scene retained: {old_ok.mean() * 100:.1f}%")
    print(f"New SCL 4/5 coverage: {scl_keep.mean() * 100:.1f}%")
    print(f"New valid NDVI coverage: {new_ok.mean() * 100:.1f}%")
    print(f"Pixels valid in both scenes: {common.sum():,} ({common.mean() * 100:.1f}%)")

    print("\n=== Different spatial samples (not a direct change estimate) ===")
    report("Old scene, old retained pixels", old)
    report("New scene, all new retained pixels", new)

    print("\n=== Identical pixel locations (descriptive temporal comparison) ===")
    report("Old scene on common pixels", old[common])
    report("New scene on common pixels", new[common])
    if common.any():
        print(f"Mean paired difference (new - old): {(new[common] - old[common]).mean():+.3f}")

    out_tif = ROOT / "sentinel_ndvi_20210206_scl_screened.tif"
    profile.update(driver="GTiff", dtype="float32", count=1,
                   nodata=NODATA, compress="deflate")
    with rasterio.open(out_tif, "w", **profile) as dst:
        dst.write(np.where(new_ok, new, NODATA).astype("float32"), 1)

    fig, axes = plt.subplots(1, 2, figsize=(11, 5), constrained_layout=True)
    for ax, arr, title in [
        (axes[0], old, "Feb 21: screened NDVI"),
        (axes[1], new, "Feb 06: screened NDVI"),
    ]:
        im = ax.imshow(arr, cmap="RdYlGn", vmin=0, vmax=0.8)
        ax.set_title(title)
        ax.set_xlabel("Pixel column")
        ax.set_ylabel("Pixel row")
    fig.colorbar(im, ax=axes, label="NDVI", shrink=0.75)
    out_png = ROOT / "sentinel_scene_comparison.png"
    fig.savefig(out_png, dpi=170)
    plt.close(fig)
    print("\nSaved:", out_tif.name)
    print("Saved:", out_png.name)
    print("Caution: different dates, and SCL is not ground truth.")


if __name__ == "__main__":
    main()
