# Sentinel-2 NDVI: Scene Quality Screening and Spatially Comparable Analysis

**A reproducible Earth observation learning project** using Sentinel-2 Level-2A imagery, Rasterio, NumPy, Matplotlib and an open STAC catalogue.

> **Project status:** Completed teaching / methods demonstration. The analysis uses actual Sentinel-2 imagery, but is not a validated vegetation-change study. The numerical results below come from runs of the scripts on the author's local Mac environment.

## Research question

**How do satellite scene selection, quality screening and spatial sampling affect NDVI estimates for the same study area?**

The project began with a cloudy image. Rather than interpret its unfiltered NDVI immediately, it used the Sentinel-2 Scene Classification Layer (SCL) to assess usable pixels, searched for clearer imagery over the *same footprint*, and compared NDVI over both all retained pixels and the identical spatial subset common to both dates.

## Data and study area

- **Source:** Sentinel-2 Level-2A Cloud Optimized GeoTIFFs (COGs), retrieved from publicly accessible imagery assets; additional scenes identified using [Element 84 Earth Search STAC API](https://earth-search.aws.element84.com/v1).
- **Original scene:** `S2B_33SVB_20210221_0_L2A` — **21 February 2021**.
- **Selected alternative:** `S2A_33SVB_20210206_1_L2A` — **6 February 2021**.
- **Tile:** `33SVB`; selected raster window begins at column 4000 and row 4000, measuring 512 × 512 pixels.
- **Geographic referencing:** `EPSG:32633` (WGS 84 / UTM zone 33N); NDVI pixel spacing 10 m × 10 m.
- **Study-window area:** approximately **26.21 km²** (262,144 pixels).
- **Bands:** B04 (red) and B08 (near-infrared), each 10 m; SCL is 20 m.

The two source scenes refer to the same geographic footprint. The window is not a randomly selected, representative ecological sample.

## Workflow

```text
Original Sentinel-2 red + NIR (10 m)
      |  NDVI = (NIR - Red) / (NIR + Red)
      v
Georeferenced NDVI GeoTIFF
      |  Inspect pixel distribution and summary statistics
      v
Original SCL quality screening (20 m -> 10 m nearest-neighbor)
      |  Retain only SCL 4 (vegetation) and 5 (not vegetated)
      v
Quantify usable coverage and masked NDVI
      |  STAC search: same tile, Feb-Apr 2021
      v
Inspect SCL for the five lowest scene-cloud candidates
      |  Select best tested local land-pixel coverage
      v
New-scene NDVI on exactly the same 10 m geographic grid
      |  Compare all retained pixels AND common valid pixel locations
      v
Evaluate spatial sampling and interpretation limits
```

**SCL screening policy:** only categories 4 and 5 are retained in this exercise. This excludes more than just clouds: unclassified, water, dark, shadow and other categories are also excluded. Therefore **“retained SCL 4/5 coverage” is not synonymous with cloud-free coverage**. SCL is an algorithmic classification, not ground truth. Resampling SCL from 20 m to 10 m does not improve its native classification resolution.

## Results

### A. First scene: before and after SCL screening

| Metric | Before screening | After retaining SCL 4/5 |
|---|---:|---:|
| Pixels used | 262,144 | 24,416 |
| Share of study window | 100.0% | **9.3%** |
| Mean NDVI | 0.251 | **0.453** |
| Median NDVI | 0.230 | **0.481** |
| Low NDVI (<0.2) | 39.8% | 4.4% |
| Moderate NDVI (0.2–<0.5) | 54.6% | 50.3% |
| High NDVI (≥0.5) | 5.6% | 45.3% |

Of 262,144 pixels in the first window, the SCL classified **83,396** as medium-probability cloud, **92,064** as high-probability cloud, and **61,808** as unclassified. Only **24,416** were in SCL classes 4 or 5. The mean change from 0.251 to 0.453 results from screening a *different set of pixels*; it is not ecological change.

### B. Searching for a clearer scene

A same-tile search returned **38 candidate items**. The five lowest scene-level cloud-score candidates were checked using their local SCL coverage. The selected item, `S2A_33SVB_20210206_1_L2A`, had **100.0% SCL 4/5 coverage within the study window**, compared with **9.3%** in the original scene.

This identifies the best tested candidate under this procedure; it does **not** establish an absolute optimum across every available scene or independent validation of cloud-free observations.

### C. Comparing different spatial samples versus matched pixels

| Comparison | Old scene (21 Feb) | New scene (6 Feb) |
|---|---:|---:|
| Retained pixels over each scene's own footprint | 24,416 | 262,144 |
| Mean NDVI on each scene's own retained pixels | 0.453 | 0.571 |
| High NDVI ≥0.5 on each scene's own retained pixels | 45.3% | 66.2% |
| **Common valid pixel locations** | **24,416** | **24,416** |
| Mean NDVI on common locations | 0.453 | 0.623 |
| Median NDVI on common locations | 0.481 | 0.654 |
| High NDVI ≥0.5 on common locations | 45.3% | 78.5% |

On the **same pixel locations**, mean NDVI on **6 February minus 21 February = +0.169**. This is a *descriptive difference between acquisitions*, **not verified vegetation change**: the observations differ in date and quality, and the old scene's small retained footprint may be biased.

## Repository files

The project uses the following scripts, in execution order:

| File | Purpose |
|---|---|
| `ndvi_demo.py` | Introductory 5 × 5 simulated red/NIR matrix and NDVI visualization (optional tutorial). |
| `real_sentinel_ndvi.py` | Read a 512 × 512 window from original scene's red/NIR COGs, calculate NDVI, and save `sentinel_ndvi.tif`. |
| `inspect_geotiff.py` | Optional inspection of CRS, dimensions, pixel resolution, data type and bounds. |
| `ndvi_distribution.py` | Analyze NDVI histogram, pixel counts, proportions and area estimates. |
| `ndvi_scl_quality.py` | Align 20 m SCL to 10 m NDVI and save `sentinel_ndvi_scl_screened.tif`. |
| `find_clear_sentinel_scenes.py` | Query Earth Search and create `selected_sentinel_scene.json` for the best tested local-coverage candidate. |
| `compare_sentinel_scenes.py` | Read the selected scene, save a new screened GeoTIFF, and compare NDVI over two spatial sampling designs. |

**Inputs generated by preceding steps:**
- `sentinel_ndvi.tif` — needed by `ndvi_distribution.py`, `ndvi_scl_quality.py`, and `find_clear_sentinel_scenes.py`.
- `sentinel_ndvi_scl_screened.tif` and `selected_sentinel_scene.json` — needed by `compare_sentinel_scenes.py`.

The Python scripts and `selected_sentinel_scene.json` are suitable for source control. Derived GeoTIFFs are excluded by the supplied project `.gitignore` because they can be regenerated. If you include PNG figures in GitHub, select only the final informative comparisons; figures do not replace downloadable georeferenced rasters for downstream analysis.

## Run locally

Tested in a macOS Python **3.9** virtual environment. Python dependencies are listed in `requirements.txt`.

From the `computational-foundations` repository root:

```bash
# If your repository already has an activated .venv, use it.
python -m pip install -r earth-observation-ndvi/requirements.txt

python earth-observation-ndvi/ndvi_demo.py                # optional tutorial
python earth-observation-ndvi/real_sentinel_ndvi.py      # original scene NDVI
python earth-observation-ndvi/ndvi_distribution.py
python earth-observation-ndvi/ndvi_scl_quality.py
python earth-observation-ndvi/find_clear_sentinel_scenes.py
python earth-observation-ndvi/compare_sentinel_scenes.py
```

The three scripts that access public remote assets require network access and availability of the STAC/COG endpoints. The `real_sentinel_ndvi.py` script should save and close a Matplotlib figure rather than leave an interactive `plt.show()` blocking execution. Most image-derived outputs can then be inspected locally without re-fetching the remote source data.

## Methodological limitations

1. **Severe filtering of the first image:** only 9.3% of original pixels pass this specific land-class screening; this subset may not represent the full area.
2. **SCL is not ground truth:** classification errors remain; category choice excludes non-vegetation land types and water, not merely cloud contamination.
3. **Cross-date comparison:** 6 February and 21 February are 15 days apart. Illumination, surface conditions, phenology and residual scene-quality effects may differ.
4. **Selection bias and denominators:** percentages on the complete new footprint and the limited old footprint answer different questions.
5. **Sensor metadata:** ensure red/NIR scaling and potential radiometric offsets are handled appropriately when adapting this workflow to other Sentinel-2 processing baselines or periods.
6. **No ecological ground validation:** NDVI describes a vegetation-greenness proxy, not vegetation health, biomass or biodiversity directly.
7. **Single small study window:** conclusions concern this processed subset and workflow, not the wider landscape.

## Key research lesson

**Scene selection and quality masking can dramatically change the spatial sample and the resulting NDVI summary.** For remote sensing comparisons, report valid coverage and compare aligned, genuinely comparable pixels before making ecological interpretations.

---

*This repository documents a learning exercise with actual satellite data and explicitly bounded conclusions. It does not claim validated vegetation change or a publishable ecological result.*
