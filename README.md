Steps to use:
1. Create new or edit existing .svg file in ./svg_files
2. Conver .svg file to .png (use Inkscape/Adobe/..)
3. Change the image filepath (line 43), output filepath (line 55). You can change the size of the object (line 22).
4. Run the blender script 
```blender --background --python create_mesh.py "png_files/grid.png" "mesh_files/grid.obj" 25
```
