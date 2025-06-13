import json
import logging
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_dimensions_from_step(step_file_path: str):
    """Extract length, breadth, and height from a STEP file"""
    reader = STEPControl_Reader()
    status = reader.ReadFile(step_file_path)

    if status != IFSelect_RetDone:
        raise Exception("Failed to read STEP file")

    reader.TransferRoots()
    shape = reader.OneShape()

    if shape.IsNull():
        raise Exception("No valid shape found in STEP file")

    # Compute bounding box
    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

    length = xmax - xmin
    breadth = ymax - ymin
    height = zmax - zmin

    return {
        'length': round(length, 3),
        'breadth': round(breadth, 3),
        'height': round(height, 3)
    }

def save_dimensions_to_json(dimensions, output_file="dimensions.json"):
    """Save extracted dimensions to a JSON file"""
    with open(output_file, 'w') as f:
        json.dump(dimensions, f, indent=4)
    print(f"\nDimensions saved to {output_file}")

if __name__ == "__main__":
    step_file = "FC30RAMD--3DModel-STEP-740395.STEP"
    try:
        dimensions = extract_dimensions_from_step(step_file)
        save_dimensions_to_json(dimensions)
    except Exception as e:
        logger.error(f"Error processing STEP file: {str(e)}")
