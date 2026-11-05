
"""Explore the distribution of a real Sentinel-2 NDVI raster."""

from pathlib import Path
import numpy as np
import rasterio
import matplotlib.pyplot as plt

FOLDER = Path(__file__).resolve().parent
INPUT = FOLDER / "sentinel_ndvi.tif"
OUTPUT = FOLDER / "ndvi_distribution.png"

# 1. Read the existing local GeoTIFF
with rasterio.open(INPUT) as src:
    ndvi = src.read(1, masked=True).astype("float32")
    crs = src.crs
    pixel_area = abs(
        src.transform.a * src.transform.e
        - src.transform.b * src.transform.d
    )

# 2. Exclude missing and invalid NDVI values
data = ndvi.filled(np.nan)
valid = np.isfinite(data) & (data >= -1) & (data <= 1)
values = data[valid]

if values.size == 0:
    raise ValueError("No valid NDVI pixels found.")

total = len(values)

print("=== Raster information ===")
print("CRS:", crs)
print("Valid pixels:", total)
print("Missing/invalid pixels:", data.size - total)

print("\n=== NDVI statistics ===")
print("Mean:", round(np.mean(values), 3))
print("Median:", round(np.median(values), 3))
print("Minimum:", round(np.min(values), 3))
print("Maximum:", round(np.max(values), 3))

# 3. Group the NDVI values
groups = [
    ("Low (< 0.2)", values < 0.2),
    ("Moderate (0.2-0.5)", (values >= 0.2) & (values < 0.5)),
    ("High (>= 0.5)", values >= 0.5),
]

print("\n=== NDVI distribution ===")

for label, condition in groups:
    count = int(np.sum(condition))
    percentage = count / total * 100
    area_km2 = count * pixel_area / 1_000_000

    print(
        f"{label}: {count:,} pixels | "
        f"{percentage:.1f}% | "
        f"{area_km2:.2f} km²"
    )

# 4. Visualize map and histogram
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

map_data = np.ma.masked_where(~valid, data)

image = axes[0].imshow(
    map_data, cmap="RdYlGn", vmin=0, vmax=0.8
)
axes[0].set_title("NDVI Map")
axes[0].set_xlabel("Pixel column")
axes[0].set_ylabel("Pixel row")
fig.colorbar(image, ax=axes[0], label="NDVI")

axes[1].hist(values, bins=40, edgecolor="black")
axes[1].axvline(0.2, linestyle="--", label="NDVI = 0.2")
axes[1].axvline(0.5, linestyle="--", label="NDVI = 0.5")
axes[1].set_title("NDVI Distribution")
axes[1].set_xlabel("NDVI")
axes[1].set_ylabel("Number of pixels")
axes[1].legend()

plt.tight_layout()
plt.savefig(OUTPUT, dpi=180)
plt.close()

print("\nSaved figure:", OUTPUT)
