# STEP File Feature Extractor

A Python tool that extracts geometric features and dimensions from STEP (ISO 10303) CAD files using pythonOCC and steputils.

## Installation

1. Create and activate a conda environment:

```bash
conda create -n step_env python=3.8
conda activate step_env
```

2. Install pythonOCC-core using conda:

```bash
conda install -c conda-forge pythonocc-core
```

3. Install steputils using pip:

```bash
pip install steputils
```

## Usage

Run the script with your STEP file:

```bash
python extract.py path/to/your/file.step
```

## Features

The tool analyzes STEP files and extracts:

- Basic properties:

  - Volume
  - Surface area
  - Bounding box dimensions

- Geometric features:

  - Cylindrical surfaces (holes, bosses)
    - Diameter
    - Location
    - Orientation
  - Planar surfaces
    - Normal direction
    - Location

- STEP entities:
  - Patterns
  - Holes
  - Extrusions

## Functions

### `analyze_shape(shape)`

- Analyzes basic properties of a shape including volume, surface area and bounding box
- Returns a dictionary with measurements

### `analyze_surface(face)`

- Analyzes individual faces to detect and measure features
- Identifies cylinders, planes and their properties

### `extract_step_features(step_file_path)`

- Main function that combines pythonOCC and steputils analysis
- Returns complete feature analysis dictionary

### `print_analysis(features)`

- Prints formatted analysis results including:
  - Overall dimensions
  - Feature counts and measurements
  - Entity statistics

## Requirements

- Python 3.8+
- pythonocc-core
- steputils
- Logging module (standard library)

## Results

The tool outputs:

```
=== STEP File Analysis ===

Dimensions:
X: min to max (range)
Y: min to max (range)
Z: min to max (range)
Volume: xxx cubic units
Surface Area: xxx square units

Cylindrical Features:
1. Diameter: xxx
   Location: (x, y, z)
...

STEP Entities:
Patterns: xxx
Holes: xxx
Extrusions: xxx
```

Results are also saved to `dimensions.json` for further processing.
