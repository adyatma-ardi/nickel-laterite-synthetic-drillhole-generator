# Automated Synthetic Nickel Laterite Drillhole Generator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GIS Integration](https://img.shields.io/badge/GIS-QGIS%20%2F%20Rasterio-green.svg)](https://qgis.org/)

An automated, industry-standard pipeline to generate synthetic drillhole databases for **Nickel Laterite Exploration**. This project bridges spatial GIS workflows (QGIS fishnet grids & DEM raster topography) with a robust Python simulation engine to produce structured subsurface data ready for geological modeling software (e.g., Leapfrog Geo, Datamine, Micromine).

---

## 🚀 Key Features

* **GIS-Integrated Collar Naming**: Utilizes QGIS Field Calculator expressions to generate unique, sequential, and localized unique identifiers (`WE-001`, `CE-001`, `EA-001`) preventing duplication errors.
* **Topographic Sampling**: Extracts exact surface elevations ($Z$) from Digital Elevation Models (DEM) via `rasterio`.
* **Laterite Profile Simulation**: Automatically models the classic vertical zonation of nickel laterite deposits:
  * **LIM** (Limonite Zone - High Fe, low-to-moderate Ni)
  * **SAP** (Saprolite Zone - High economic Ni grades)
  * **BRK** (Bedrock / Serpentinite / Peridotite substrate)
* **Geostatistical Constraints**: Simulates realistic grade distributions for **Ni**, **Co**, and **Fe** using normal distributions with controlled variance and anomaly injections.
* **Automated Bash Pipeline**: Streamlines execution via an interactive/autonomous Bash wrapper script.

---

## 📂 Project Directory Structure

```text
nickel-laterite-drillhole-generator/
│
├── raw_data/                  # Input folder for raw spatial data
│   ├── dem_topography.tif     # DEM raster file (.tif)
│   └── combined_grid.csv      # Fishnet grid collars with unique Hole_IDs (.csv)
│
├── output_database/           # Generated industry-standard relational tables
│   ├── collar.csv             # Collar coordinates, total depth, and elevation
│   ├── survey.csv             # Downhole survey data (Azimuth, Dip)
│   ├── geology.csv            # Lithological intervals (LIM, SAP, BRK)
│   └── assay.csv              # Grade intervals (Ni_pct, Co_pct, Fe_pct)
│
├── generate_drillholes.py     # Core Python processing & simulation engine
├── run_pipeline.sh            # Automated Bash execution wrapper
└── requirements.txt           # Required Python libraries
