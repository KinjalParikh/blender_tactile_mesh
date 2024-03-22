import bpy


def generate_mesh(image_path, output_path, size):
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
    cube_obj.scale = (size, size, 1)
    
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
    bpy.ops.image.open(filepath=image_path)
    image = bpy.data.images.load(image_path)
    
    # Assign the loaded image as the displacement map for the vertex group
    displace_modifier = cube_obj.modifiers.new(name="Displace", type='DISPLACE')
    displace_modifier.direction = 'Z'
    displace_modifier.vertex_group = vertex_group.name
    displace_modifier.texture = bpy.data.textures.new(name="Displace_Texture", type='IMAGE')
    displace_modifier.texture.image = image
    
    # Set up file output parameters
    
    # Export the mesh as an OBJ file
    if output_path.endswith(".obj"):
        print("Saving as OBJ")
        bpy.ops.export_scene.obj(filepath=output_path, use_selection=True)
    else:
        print("Saving as STL")
        bpy.ops.export_mesh.stl(filepath=output_path, use_selection=True)


if __name__ == "__main__":
    # args = sys.argv
    #
    # image_path = "png_files/grid.png" if args[4] is None else args[4]
    # output_path = "mesh_files/grid.stl" if args[5] is None else args[5]
    # size = 25 if args[6] is None else int(args[6])
    size = 50
    density = [0.95+i*(0.025/6) for i in range(7)]
    pattern = ["lines", "grid"] #, "dots"]

    print("Generating meshes")
    for p in pattern:
        for d in density:
            print("Size: ", size, " Density: ", density, " Pattern: ", pattern)
            image_path = "png_files/{}_size{}_density{:.3f}.png".format(p, 400, d)
            output_path = "mesh_files/{}_size{}_density{:.3f}.obj".format(p, size, d)
            generate_mesh(image_path, output_path, size)