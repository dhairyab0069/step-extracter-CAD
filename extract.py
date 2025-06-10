import steputils.p21 as p21
from OCC.Core import STEPControl_Reader, TopExp_Explorer, TopAbs_SOLID, TopAbs_FACE, TopAbs_EDGE
from OCC.Core import BRep_Tool, GeomLProp_SLProps, BRepGProp_Face, GProp_GProps
from OCC.Core import BRepBndLib_Add, Bnd_Box
from OCC.Extend.TopologyUtils import TopologyExplorer
import math

def extract_step_dimensions(step_file_path):
    """Extract dimensions and geometric properties from a STEP file"""
    
    # Method 1: Using steputils for entity analysis
    print("=== STEP File Entity Analysis ===")
    step_model = p21.readfile(step_file_path)
    
    # Extract coordinate points for bounding analysis
    coordinates = []
    cylindrical_radii = []
    
    for entity in step_model.values():
        # Extract Cartesian points
        if hasattr(entity, 'type_name') and entity.type_name == 'CARTESIAN_POINT':
            if hasattr(entity, 'coordinates'):
                coords = entity.coordinates
                coordinates.append([float(c) for c in coords])
        
        # Extract cylindrical surface radii
        elif hasattr(entity, 'type_name') and entity.type_name == 'CYLINDRICAL_SURFACE':
            if hasattr(entity, 'radius'):
                cylindrical_radii.append(float(entity.radius))
    
    # Calculate bounding box from coordinates
    if coordinates:
        x_coords = [c[0] for c in coordinates]
        y_coords = [c[1] for c in coordinates]
        z_coords = [c[2] for c in coordinates]
        
        bbox_dimensions = {
            'x_min': min(x_coords),
            'x_max': max(x_coords),
            'y_min': min(y_coords),
            'y_max': max(y_coords),
            'z_min': min(z_coords),
            'z_max': max(z_coords),
            'x_range': max(x_coords) - min(x_coords),
            'y_range': max(y_coords) - min(y_coords),
            'z_range': max(z_coords) - min(z_coords)
        }
        
        print(f"Bounding Box Dimensions:")
        print(f"  X: {bbox_dimensions['x_min']:.3f} to {bbox_dimensions['x_max']:.3f} (range: {bbox_dimensions['x_range']:.3f})")
        print(f"  Y: {bbox_dimensions['y_min']:.3f} to {bbox_dimensions['y_max']:.3f} (range: {bbox_dimensions['y_range']:.3f})")
        print(f"  Z: {bbox_dimensions['z_min']:.3f} to {bbox_dimensions['z_max']:.3f} (range: {bbox_dimensions['z_range']:.3f})")
    
    # Extract cylindrical features
    if cylindrical_radii:
        unique_radii = list(set(cylindrical_radii))
        print(f"\nCylindrical Features:")
        for radius in sorted(unique_radii):
            count = cylindrical_radii.count(radius)
            diameter = radius * 2
            print(f"  Radius: {radius:.3f} mm (Diameter: {diameter:.3f} mm) - Count: {count}")
    
    # Method 2: Using pythonocc-core for geometric analysis
    print("\n=== PyOCC Geometric Analysis ===")
    
    # Read STEP file with pythonocc
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(step_file_path)
    
    if status == 1:  # Success
        step_reader.TransferRoots()
        shape = step_reader.OneShape()
        
        # Calculate precise bounding box
        bbox = Bnd_Box()
        BRepBndLib_Add(shape, bbox)
        
        if not bbox.IsVoid():
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            
            print(f"Precise Bounding Box:")
            print(f"  X: {xmin:.3f} to {xmax:.3f} (range: {xmax-xmin:.3f})")
            print(f"  Y: {ymin:.3f} to {ymax:.3f} (range: {ymax-ymin:.3f})")
            print(f"  Z: {zmin:.3f} to {zmax:.3f} (range: {zmax-zmin:.3f})")
            print(f"  Volume Envelope: {(xmax-xmin) * (ymax-ymin) * (zmax-zmin):.3f} cubic units")
        
        # Analyze topology
        topo_explorer = TopologyExplorer(shape)
        
        print(f"\nTopological Analysis:")
        print(f"  Solids: {topo_explorer.number_of_solids()}")
        print(f"  Faces: {topo_explorer.number_of_faces()}")
        print(f"  Edges: {topo_explorer.number_of_edges()}")
        print(f"  Vertices: {topo_explorer.number_of_vertices()}")
        
        # Calculate surface areas and volumes
        total_surface_area = 0
        total_volume = 0
        
        for solid in topo_explorer.solids():
            # Calculate volume
            props = GProp_GProps()
            from OCC.Core import BRepGProp_VolumeProperties
            BRepGProp_VolumeProperties(solid, props)
            volume = props.Mass()
            total_volume += volume
            
            # Calculate surface area
            surface_props = GProp_GProps()
            from OCC.Core import BRepGProp_SurfaceProperties
            BRepGProp_SurfaceProperties(solid, surface_props)
            surface_area = surface_props.Mass()
            total_surface_area += surface_area
        
        print(f"\nPhysical Properties:")
        print(f"  Total Volume: {total_volume:.3f} cubic units")
        print(f"  Total Surface Area: {total_surface_area:.3f} square units")
        
        return {
            'bounding_box': bbox_dimensions if coordinates else None,
            'cylindrical_features': unique_radii if cylindrical_radii else [],
            'topology': {
                'solids': topo_explorer.number_of_solids(),
                'faces': topo_explorer.number_of_faces(),
                'edges': topo_explorer.number_of_edges(),
                'vertices': topo_explorer.number_of_vertices()
            },
            'physical_properties': {
                'volume': total_volume,
                'surface_area': total_surface_area
            }
        }
    
    else:
        print("Failed to read STEP file")
        return None

# Advanced feature extraction
def extract_detailed_features(step_file_path):
    """Extract more detailed geometric features"""
    
    step_model = p21.readfile(step_file_path)
    
    features = {
        'holes': [],
        'bosses': [],
        'planes': [],
        'curves': [],
        'patterns': []
    }
    
    for entity_id, entity in step_model.items():
        if hasattr(entity, 'type_name'):
            # Look for hole patterns (cylindrical surfaces with small radii)
            if entity.type_name == 'CYLINDRICAL_SURFACE':
                if hasattr(entity, 'radius'):
                    radius = float(entity.radius)
                    if radius < 1.0:  # Assuming holes are < 1mm radius
                        features['holes'].append({
                            'radius': radius,
                            'diameter': radius * 2,
                            'entity_id': entity_id
                        })
            
            # Look for extrusion features
            elif 'EXTRUDE' in entity.type_name or 'BOSS' in str(entity):
                features['bosses'].append(entity_id)
            
            # Look for planar surfaces
            elif entity.type_name == 'PLANE':
                features['planes'].append(entity_id)
            
            # Look for pattern references
            elif 'PATTERN' in str(entity) or 'LPattern' in str(entity):
                features['patterns'].append(entity_id)
    
    return features

# Usage example
if __name__ == "__main__":
    step_file = "FC30RAMD--3DModel-STEP-740395.STEP"  # Replace with your STEP file path
    
    try:
        # Extract basic dimensions
        dimensions = extract_step_dimensions(step_file)
        
        # Extract detailed features
        print("\n=== Detailed Feature Analysis ===")
        features = extract_detailed_features(step_file)
        
        if features['holes']:
            print(f"Detected Holes:")
            for i, hole in enumerate(features['holes']):
                print(f"  Hole {i+1}: Diameter {hole['diameter']:.3f} mm")
        
        if features['patterns']:
            print(f"Pattern Features: {len(features['patterns'])} detected")
        
        print(f"Planar Surfaces: {len(features['planes'])}")
        
    except Exception as e:
        print(f"Error processing STEP file: {e}")
