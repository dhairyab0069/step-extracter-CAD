# CAD File Feature Extractor (WIP 🚧)

> ⚠️ **Work in Progress**
> This tool is under active development. Feature support, output formats, and architecture may evolve.

---

## Overview

**CAD File Feature Extractor** is a Python-based tool that extracts geometric features and dimensional properties from CAD files (STEP, IGES, STL) using `pythonOCC`.

The goal is to provide automated geometric analysis for engineering workflows, manufacturing validation, and downstream computational processing.

---

## Supported File Formats

* STEP (.step, .stp)
* IGES (.iges, .igs)
* STL (.stl)

---

## Installation

### 1. Create and Activate a Conda Environment

```bash
conda create -n pyocct python=3.8
conda activate pyocct
```

### 2. Install pythonOCC-core

```bash
conda install -c conda-forge pythonocc-core
```

---

## Usage

Run the extraction script with your CAD file:

```bash
python extract.py
```

---

## Features (Current Scope)

### 📏 Basic Dimensions

* Length
* Breadth
* Height
* Volume
* Surface Area

### 🔵 Geometric Features

* Cylindrical Features (holes, bosses)

  * Diameter
  * Location coordinates (x, y, z)
* Bounding box dimensions

---

## Output Files

The tool generates two output files per processed model:

### 1. `{filename}_dimensions.json`

* Basic dimensional data
* Length, breadth, height
* Structured JSON format for downstream use

### 2. `{filename}_analysis.txt`

* Full dimensional ranges (X, Y, Z)
* Volume and surface area
* Detailed list of cylindrical features with locations

---

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

---

## Requirements

* Python 3.8+
* pythonocc-core
* Standard Python libraries:

  * json
  * logging

---

## Error Handling

Includes safeguards for:

* Invalid or unsupported file formats
* Missing files
* Corrupted CAD data
* Empty or invalid geometric shapes

---

## Roadmap (Planned Enhancements)

* [ ] Feature classification beyond cylindrical geometry
* [ ] Support for additional analytic feature detection (slots, fillets, pockets)
* [ ] Batch processing support
* [ ] API layer for integration with larger systems
* [ ] Performance optimization for large assemblies

---

## License

[License information to be added]

---

🚀 This project is actively evolving. Contributions and experiment
