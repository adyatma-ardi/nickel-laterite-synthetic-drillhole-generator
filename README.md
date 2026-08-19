# Automated Synthetic Nickel Laterite Drillhole Generator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GIS Integration](https://img.shields.io/badge/GIS-QGIS%20%2F%20Rasterio-green.svg)](https://qgis.org/)

An automated, industry-standard pipeline to generate synthetic drillhole databases for **Nickel Laterite Exploration**. This project bridges spatial GIS workflows (QGIS fishnet grids & DEM raster topography) with a robust Python simulation engine to produce structured subsurface data ready for geological modeling software (e.g., Leapfrog Geo, Datamine, Micromine) and GIS analysis.

---

## 🚀 Key Features

* **Topographic Sampling**: Extracts exact surface elevations (Z) directly from Digital Elevation Models (DEM) using `rasterio`.
* **Synchronized Survey Depths**: Automatically aligns the downhole survey terminal depths with the maximum collar depth (`max_depth`) for 100% data consistency.
* **Laterite Profile Simulation**: Models the classic vertical zonation of nickel laterite deposits based on elevation trends:
  * **LIM** (Limonite Zone - High Fe, low-to-moderate Ni, low MgO)
  * **SAP** (Saprolite Zone - High economic Ni grades, moderate MgO & SiO2)
  * **BRK** (Bedrock / Serpentinite / Peridotite substrate - High MgO & SiO2, low Fe)
* **Comprehensive Multi-Element Assay Simulation**: Generates realistic geostatistical grade distributions for **Ni**, **Co**, **Fe**, **MgO**, and **SiO2** with controlled variance and anomaly injections.
* **Unique Sample Identifiers**: Integrates sequential `samp_id` strings (e.g., `Hole_ID/01`) seamlessly across both geological and assay intervals.

---

## 📂 Project Directory Structure

```text
nickel-laterite-drillhole-generator/
│
├── raw_data/                  # Input folder for raw spatial data
│   ├── dem_topography.tif     # DEM raster file (.tif)
│   └── combined_grid.csv      # Fishnet grid collars exported from QGIS (.csv)
│
├── output_database/           # Generated industry-standard relational tables
│   ├── collar.csv             # Main collar locations and depths
│   ├── survey.csv             # Downhole survey data (Dip, Azimuth)
│   ├── geology.csv            # Lithological intervals (LIM, SAP, BRK)
│   └── assay.csv              # Multi-element chemistry intervals
│
├── generate_drillholes.py     # Core Python processing & simulation engine
├── run_pipeline.bat           # Automated Windows Batch execution wrapper (Recommended)
├── run_pipeline.sh            # Automated Bash execution wrapper (Linux/macOS)
└── requirements.txt           # Required Python libraries
```

---

## ⚙️ Prerequisites & Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/nickel-laterite-drillhole-generator.git
    cd nickel-laterite-drillhole-generator
    ```

2. **Install dependencies:**

    **Option A: Install via requirements file (Recommended)**
    ```bash
    pip install -r requirements.txt
    ```

    **Option B: Install directly via PIP**
    ```bash
    pip install numpy pandas rasterio
    ```

---

## 🛠️ Workflow & How to Run

### Step 1: QGIS Spatial Preparation

1. Generate a fishnet drillhole grid over your study domains in QGIS.
2. Ensure your grid attribute table contains already-formatted unique identification codes under the column `Hole_ID`, alongside coordinate columns `X` and `Y`.
3. Export the attribute table as a CSV file (`combined_grid.csv`).

### Step 2: Organize Raw Data

Place your prepared input files inside the `./raw_data/` directory:
* Your terrain elevation model (`dem_topography.tif`)
* Your exported grid CSV (`combined_grid.csv`)

### Step 3: Execute the Generator Pipeline

#### For Windows Users (Recommended)
Double-click the **`run_pipeline.bat`** file from your File Explorer, or execute it via Command Prompt (CMD):
```cmd
run_pipeline.bat
```

#### For Linux / macOS Users
Run the automation script from your terminal interface:
```bash
bash run_pipeline.sh
```

The workflow will automatically validate folders, check and install missing library dependencies, sample surface elevations from your DEM, run downhole geochemical profiles, and write standardized database files into `./output_database/`.

---

## 📊 Output Data Schema

The exported tables feature clean, lowercase layouts strictly engineered for smooth geostatistical and GIS processing integrations:

### 📍 `collar.csv`
Contains core coordinate geometry data and drilling limits.
* `hole_id`: Unique identification tag.
* `y`: Northing grid coordinate.
* `x`: Easting grid coordinate.
* `z`: Surface elevation meters sampled from DEM.
* `max_depth`: Calculated full penetration length.

### 📐 `survey.csv`
Defines downhole geometry vectors (defaulting to vertical exploration holes).
* `hole_id`: Unique identification tag.
* `depth`: Terminal distance (automatically matched with collar `max_depth`).
* `dip`: Inclination tilt (vertical exploration at `-90.0`).
* `azimuth`: Compass direction heading (`0.0`).

### 🪵 `geology.csv`
Defines physical rock classification domains.
* `hole_id`: Unique identification tag.
* `samp_id`: Interval sample identifier (`Hole_ID/Counter`).
* `depth_from`: Start depth of geological layer.
* `depth_to`: End depth of geological layer.
* `lithology`: Material zone designation (`LIM`, `SAP`, or `BRK`).

### 🧪 `assay.csv`
Quantifies grade elements matching identical geological limits.
* `hole_id`: Unique identification tag.
* `samp_id`: Interval sample identifier (`Hole_ID/Counter`).
* `depth_from`: Start depth of grade interval.
* `depth_to`: End depth of grade interval.
* `ni`: Nickel grade percentages.
* `co`: Cobalt grade percentages.
* `fe`: Iron grade percentages.
* `mgo`: Magnesium oxide percentages.
* `sio2`: Silica dioxide percentages.

---

## 📄 License

This project is open-source under the MIT License.
