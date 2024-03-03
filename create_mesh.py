import bpy
import os

# Set scene units to metric with millimeter units
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'

# Clear existing objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create a new mesh object
bpy.ops.mesh.primitive_cube_add(size=1)

# Get the created cube object
cube_obj = bpy.context.object

# Scale the cube to desired dimensions
cube_obj.scale = (25, 25, 1)

# Remesh the mesh for better deformation
bpy.ops.object.modifier_add(type='REMESH')
remesh_modifier = cube_obj.modifiers["Remesh"]
remesh_modifier.octree_depth = 8  # Adjust remesh depth as needed
remesh_modifier.mode = 'SMOOTH'  # Choose remesh mode as needed

# Apply the remesh modifier to the mesh
bpy.ops.object.modifier_apply(modifier=remesh_modifier.name)

# Create a new vertex group
vertex_group = cube_obj.vertex_groups.new(name="Z_Up_Vertices")

# Get the mesh data of the cube
mesh = cube_obj.data

# Iterate through each vertex and add it to the vertex group if its normal points up
for vertex in mesh.vertices:
    if vertex.normal[2] > 0.5:   # Check if normal direction points upwards
        vertex_group.add([vertex.index], 1.0, 'REPLACE')

# Load an image as a displacement map
image_path = "png_files/dots.png"
bpy.ops.image.open(filepath=image_path)
image = bpy.data.images.load(image_path)

# Assign the loaded image as the displacement map for the vertex group
displace_modifier = cube_obj.modifiers.new(name="Displace", type='DISPLACE')
displace_modifier.direction = 'Z'
displace_modifier.vertex_group = vertex_group.name
displace_modifier.texture = bpy.data.textures.new(name="Displace_Texture", type='IMAGE')
displace_modifier.texture.image = image

# Set up file output parameters
output_path = "mesh_files/dots.obj"

# Export the mesh as an OBJ file
bpy.ops.export_scene.obj(filepath=output_path, use_selection=True)
