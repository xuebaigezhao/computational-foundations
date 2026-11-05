
from pathlib import Path

import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.windows import Window

# Public Sentinel-2B L2A imagery, 21 February 2021.
BASE = (
    "https://sentinel-cogs.s3.us-west-2.amazonaws.com/"
    "sentinel-s2-l2a-cogs/33/S/VB/2021/2/"
    "S2B_33SVB_20210221_0_L2A/"
)

RED_URL = BASE + "B04.tif"
NIR_URL = BASE + "B08.tif"

# A 512 x 512 pixel region (about 5.12 km x 5.12 km).
window = Window(4000, 4000, 512, 512)

output_dir = Path(__file__).resolve().parent

with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
    with rasterio.open(RED_URL) as red_src, \
         rasterio.open(NIR_URL) as nir_src:

        assert red_src.crs == nir_src.crs
        assert red_src.transform == nir_src.transform

        red = red_src.read(
            1, window=window, masked=True
        ).astype("float32")

        nir = nir_src.read(
            1, window=window, masked=True
        ).astype("float32")

        # Save geographical metadata for the output.
        profile = red_src.profile.copy()
        profile.update(
            driver="GTiff",
            height=512,
            width=512,
            count=1,
            dtype="float32",
            transform=red_src.window_transform(window),
            nodata=-9999.0,
            compress="deflate",
        )

        print("CRS:", red_src.crs)
        print("Pixel size:", red_src.res)
        print("Selected window:", window)

# NDVI calculation, ignoring no-data and zero denominators.
denominator = nir + red
ndvi = np.ma.divide(nir - red, denominator)
ndvi = np.ma.masked_where(denominator <= 0, ndvi)
ndvi_array = ndvi.filled(np.nan).astype("float32")

# Save a geographically referenced raster.
geotiff_path = output_dir / "sentinel_ndvi.tif"

raster_values = np.where(
    np.isfinite(ndvi_array), ndvi_array, -9999.0
).astype("float32")

with rasterio.open(geotiff_path, "w", **profile) as dst:
    dst.write(raster_values, 1)

# Save a preview image.
plt.figure(figsize=(7, 6))
plt.imshow(ndvi_array, cmap="RdYlGn", vmin=-1, vmax=1)
plt.colorbar(label="NDVI")
plt.title("Sentinel-2B NDVI — Sicily, 2021-02-21")
plt.xlabel("Pixel column")
plt.ylabel("Pixel row")
plt.tight_layout()
plt.savefig(output_dir / "sentinel_ndvi.png", dpi=180)
plt.close()

print("Mean NDVI:", round(np.nanmean(ndvi_array), 3))
print("Saved GeoTIFF:", geotiff_path)
print("Saved preview: sentinel_ndvi.png")

print("Minimum NDVI:", round(np.nanmin(ndvi_array), 3))
print("Median NDVI:", round(np.nanmedian(ndvi_array), 3))
print("Maximum NDVI:", round(np.nanmax(ndvi_array), 3))
