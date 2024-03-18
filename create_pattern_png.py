import os
from PIL import Image, ImageDraw

def create_lines(size, density):
    file_name = "lines_size{}_density{}.png".format(size, density)
    out_dir = "./png_files/"
    opath = os.path.join(out_dir, file_name)

    img = Image.new("RGB", (size, size), "black")
    draw = ImageDraw.Draw(img)

    step = int((1-density)*size//2)
    for i in range(1, size, step):
        draw.line((0, i, size, i), fill="white")

    img.save(opath)


def create_grid(size, density):
    file_name = "grid_size{}_density{}.png".format(size, density)
    out_dir = "./png_files/"
    opath = os.path.join(out_dir, file_name)

    img = Image.new("RGB", (size, size), "black")
    draw = ImageDraw.Draw(img)

    step = int((1 - density) * size//2)
    for i in range(1, size, step):
        draw.line((0, i, size, i), fill="white")
        draw.line((i, 0, i, size), fill="white")

    img.save(opath)


def create_dots(size, density):
    file_name = "dots_size{}_density{}.png".format(size, density)
    out_dir = "./png_files/"
    opath = os.path.join(out_dir, file_name)

    img = Image.new("RGB", (size, size), "black")
    draw = ImageDraw.Draw(img)

    step = int((1 - density) * size//2)
    for i in range(1, size, step):
        for j in range(1, size, step):
            draw.ellipse((i-1.5, j-1.5, i+1.5, j+1.5), fill="white")

    img.save(opath)


def create_png(size, density, pattern="lines"):
    print("Size: ", size, " Density: ", density, " Pattern: ", pattern)
    if pattern == "lines":
        create_lines(size, density)
    elif pattern == "grid":
        create_grid(size, density)
    elif pattern == "dots":
        create_dots(size, density)
    else:
        raise ValueError("Invalid pattern type")


if __name__ == "__main__":
    size = 400
    density = [0.85, 0.875, 0.9, 0.925, 0.95]
    pattern = ["lines", "grid", "dots"]

    print("Creating PNGs")
    for p in pattern:
        for d in density:
            create_png(size, d, p)