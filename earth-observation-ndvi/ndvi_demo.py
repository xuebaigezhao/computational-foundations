
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Simulated reflectance values for two satellite bands.
# Each number represents one pixel.

red = np.array([
    [0.30, 0.28, 0.25, 0.24, 0.30],
    [0.26, 0.15, 0.12, 0.16, 0.29],
    [0.25, 0.12, 0.08, 0.13, 0.27],
    [0.29, 0.16, 0.11, 0.15, 0.28],
    [0.31, 0.30, 0.26, 0.29, 0.32]
])

nir = np.array([
    [0.34, 0.38, 0.40, 0.39, 0.34],
    [0.41, 0.55, 0.62, 0.53, 0.40],
    [0.42, 0.64, 0.72, 0.63, 0.41],
    [0.38, 0.54, 0.66, 0.55, 0.39],
    [0.33, 0.35, 0.38, 0.36, 0.34]
])

# Calculate NDVI for every pixel.
denominator = nir + red

ndvi = np.divide(
    nir - red,
    denominator,
    out=np.full_like(red, np.nan),
    where=denominator != 0
)

print("NDVI matrix:")
print(np.round(ndvi, 2))

print("Mean NDVI:", round(np.nanmean(ndvi), 3))
print("Maximum NDVI:", round(np.nanmax(ndvi), 3))

# Visualize the three rasters.
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, data, title, cmap, low, high in [
    (axes[0], red, "Red band", "Reds", 0, 0.75),
    (axes[1], nir, "NIR band", "Greys", 0, 0.75),
    (axes[2], ndvi, "NDVI", "RdYlGn", -1, 1),
]:
    image = ax.imshow(data, cmap=cmap, vmin=low, vmax=high)
    ax.set_title(title)
    ax.set_xlabel("Pixel column")
    ax.set_ylabel("Pixel row")
    fig.colorbar(image, ax=ax, shrink=0.7)

plt.tight_layout()

output = Path(__file__).with_name("ndvi_demo.png")
plt.savefig(output, dpi=180)
plt.show()

print("Saved figure:", output)
print("Minimum NDVI:", round(np.nanmin(ndvi_array), 3))
print("Median NDVI:", round(np.nanmedian(ndvi_array), 3))
print("Maximum NDVI:", round(np.nanmax(ndvi_array), 3))