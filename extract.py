import json
import logging
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IGESControl import IGESControl_Reader
from OCC.Core.StlAPI import StlAPI_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Circle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _round_dimensions(bbox):
    """Utility function to calculate rounded dimensions from bounding box"""
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    return {
        'length': round(xmax - xmin, 3),
        'breadth': round(ymax - ymin, 3),
        'height': round(zmax - zmin, 3)
    }

def analyze_shape(shape):
    """Analyze shape and return detailed properties"""
    # Calculate basic properties
    props = GProp_GProps()
    brepgprop.VolumeProperties(shape, props)
    volume = props.Mass()
    
    brepgprop.SurfaceProperties(shape, props)
    surface_area = props.Mass()
    
    # Calculate bounding box
    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    
    # Find cylindrical features
    cylinders = []
    exp = TopExp_Explorer(shape, TopAbs_EDGE)
    
    while exp.More():
        edge = exp.Current()
        curve_handle = BRep_Tool().Curve(edge)[0]
        adaptor = GeomAdaptor_Curve(curve_handle)
        
        if adaptor.GetType() == GeomAbs_Circle:
            circle = adaptor.Circle()
            location = circle.Location()
            diameter = circle.Radius() * 2
            cylinders.append({
                'diameter': round(diameter, 3),
                'location': (
                    round(location.X(), 3),
                    round(location.Y(), 3),
                    round(location.Z(), 3)
                )
            })
        exp.Next()
    
    return {
        'dimensions': {
            'x_range': (round(xmin, 3), round(xmax, 3), round(xmax - xmin, 3)),
            'y_range': (round(ymin, 3), round(ymax, 3), round(ymax - ymin, 3)),
            'z_range': (round(zmin, 3), round(zmax, 3), round(zmax - zmin, 3)),
        },
        'volume': round(volume, 3),
        'surface_area': round(surface_area, 3),
        'cylinders': cylinders
    }

def save_detailed_analysis(analysis, file_path):
    """Save detailed analysis to a text file"""
    base_name = file_path.rsplit('.', 1)[0]
    output_file = f"{base_name}_analysis.txt"
    
    with open(output_file, 'w') as f:
        f.write(f"=== {file_path} Analysis ===\n\n")
        f.write("Dimensions:\n")
        dims = analysis['dimensions']
        f.write(f"X: {dims['x_range'][0]} to {dims['x_range'][1]} (range: {dims['x_range'][2]})\n")
        f.write(f"Y: {dims['y_range'][0]} to {dims['y_range'][1]} (range: {dims['y_range'][2]})\n")
        f.write(f"Z: {dims['z_range'][0]} to {dims['z_range'][1]} (range: {dims['z_range'][2]})\n\n")
        
        f.write(f"Volume: {analysis['volume']} cubic units\n")
        f.write(f"Surface Area: {analysis['surface_area']} square units\n\n")
        
        f.write("Cylindrical Features:\n")
        for i, cyl in enumerate(analysis['cylinders'], 1):
            f.write(f"  {i}. Diameter: {cyl['diameter']}\n")
            f.write(f"     Location: {cyl['location']}\n")
    
    print(f"\nDetailed analysis saved to {output_file}")

def extract_dimensions_from_step(step_file_path: str):
    """Extract dimensions from a STEP file"""
    reader = STEPControl_Reader()
    status = reader.ReadFile(step_file_path)

    if status != IFSelect_RetDone:
        raise Exception("Failed to read STEP file")

    reader.TransferRoots()
    shape = reader.OneShape()

    if shape.IsNull():
        raise Exception("No valid shape found in STEP file")

    analysis = analyze_shape(shape)
    save_detailed_analysis(analysis, step_file_path)
    return analysis['dimensions']

def extract_dimensions_from_iges(iges_file_path: str):
    """Extract dimensions from an IGES file"""
    reader = IGESControl_Reader()
    status = reader.ReadFile(iges_file_path)

    if status != IFSelect_RetDone:
        raise Exception("Failed to read IGES file")

    reader.TransferRoots()
    shape = reader.OneShape()

    if shape.IsNull():
        raise Exception("No valid shape found in IGES file")

    analysis = analyze_shape(shape)
    save_detailed_analysis(analysis, iges_file_path)
    return analysis['dimensions']

def extract_dimensions_from_stl(stl_file_path: str):
    """Extract dimensions from an STL file"""
    reader = StlAPI_Reader()
    shape = TopoDS_Shape()
    status = reader.Read(shape, stl_file_path)

    if not status or shape.IsNull():
        raise Exception("Failed to read STL file or no valid shape found")

    analysis = analyze_shape(shape)
    save_detailed_analysis(analysis, stl_file_path)
    return analysis['dimensions']

def save_dimensions_to_json(dimensions, file_path):
    """Save extracted dimensions to a JSON file"""
    # Extract filename without extension
    base_name = file_path.rsplit('.', 1)[0]
    output_file = f"{base_name}_dimensions.json"
    
    with open(output_file, 'w') as f:
        json.dump(dimensions, f, indent=4)
    print(f"\nDimensions saved to {output_file}")

if __name__ == "__main__":
    try:
        # step path
        step_file_path = "FC30RAMD--3DModel-STEP-740395.STEP"
        step_dims = extract_dimensions_from_step(step_file_path)
        save_dimensions_to_json(step_dims, step_file_path)

        # iges path
        iges_file_path = "10774.igs"
        iges_dims = extract_dimensions_from_iges(iges_file_path)
        save_dimensions_to_json(iges_dims, iges_file_path)

        # STL processing commented out
        # stl_file_path = "model.stl"
        # stl_dims = extract_dimensions_from_stl(stl_file_path)
        # save_dimensions_to_json(stl_dims, stl_file_path)

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
