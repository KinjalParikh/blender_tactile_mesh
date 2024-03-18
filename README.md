Steps to use:
1. Create patterns using create_pattern_png.py (change line 66, 67). Leave the size as is.
    ```
    python create_pattern_png.py
    ```
    This will create a pattern in the folder `pattern` and a mask in the folder `mask`. The mask is used to create the mesh.
2. Generate the mesh using create_mesh.py (make changes in line 71 to 73 corresponding to the pattern created in step 1):
    ```
    blender --background --python create_mesh.py
    ```

Note: No command line arguments are available for the scripts. The user has to make changes in the script itself.