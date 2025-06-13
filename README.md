# CAD File Feature Extractor

A Python tool that extracts geometric features and dimensions from CAD files (STEP, IGES, STL) using pythonOCC.

## Installation

1. Create and activate a conda environment:

```bash
conda create -n pyocct python=3.8
conda activate pyocct
```

2. Install pythonOCC-core using conda:

```bash
conda install -c conda-forge pythonocc-core
```

## Supported File Formats

- STEP (.step, .stp)
- IGES (.iges, .igs)
- STL (.stl)

## Usage

Run the script with your CAD file:

```bash
python extract.py
```

## Features

The tool analyzes CAD files and extracts:

- Basic Dimensions:

  - Length
  - Breadth
  - Height
  - Volume
  - Surface area

- Geometric Features:
  - Cylindrical features (holes, bosses)
    - Diameter
    - Location coordinates (x, y, z)
  - Bounding box dimensions

## Output Files

The tool generates two output files:

1. `{filename}_dimensions.json`:

   - Contains basic dimensional data in JSON format
   - Includes length, breadth, and height

2. `{filename}_analysis.txt`:
   - Detailed analysis report including:
     - Full dimensional ranges (X, Y, Z)
     - Volume and surface area
     - Complete list of cylindrical features with locations

## Example Output

```markdown
=== STEP File Analysis ===

Dimensions:
X: -6.000 to 6.000 (range: 12.000)
Y: -0.000 to 2.300 (range: 2.300)
Z: -6.000 to 6.000 (range: 12.000)

Volume: 112.467 cubic units
Surface Area: 808.267 square units

Cylindrical Features:

1. Diameter: 1.000
   Location: (-3.750, -0.001, -4.050)
   ...
```

## Requirements

- Python 3.8+
- pythonocc-core
- Standard Python libraries:
  - json
  - logging

## Error Handling

The tool includes robust error handling for:

- Invalid file formats
- Missing files
- Corrupted CAD data
- Empty or invalid shapes

## License

[Your License Information]
