import os


def create_lines(size):
    file_name = "lines_{}.svg".format(size)
    out_dir = "./svg_files/"
    opath = os.path.join(out_dir, file_name)

    with open(opath, "w") as svg_file:
        svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}mm" height="{size}mm" viewBox="0 0 {size} {size}">\n')
        svg_file.write('    <defs>\n')
        svg_file.write('        <pattern id="lines_pattern" width="0.5mm" height="3mm" patternUnits="userSpaceOnUse">\n')
        svg_file.write('            <rect width="0.5mm" height="3mm" fill="black"/>\n')
        svg_file.write('            <line x1="-1mm" y1="1.25mm" x2="1.5mm" y2="1.25mm" stroke="white"/>\n')
        svg_file.write('        </pattern>\n')
        svg_file.write('    </defs>\n')
        svg_file.write('    <rect x="0" y="0" width="100%" height="100%" fill="url(#lines_pattern)"/>\n')
        svg_file.write('</svg>\n')


def create_grid(size):
    file_name = "grid_{}.svg".format(size)
    out_dir = "./svg_files/"
    opath = os.path.join(out_dir, file_name)

    with open(opath, "w") as svg_file:
        svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}mm" height="{size}mm" viewBox="0 0 {size} {size}">\n')
        svg_file.write('    <defs>\n')
        svg_file.write('        <pattern id="grid_pattern" width="1mm" height="1mm" patternUnits="userSpaceOnUse">\n')
        svg_file.write('            <rect width="1mm" height="1mm" fill="black"/>\n')
        svg_file.write('            <line x1="-1mm" y1="0.5mm" x2="2mm" y2="0.5mm" stroke="white"/>\n')
        svg_file.write('            <line x1="0.5mm" y1="-1mm" x2="0.5mm" y2="2mm" stroke="white"/>\n')
        svg_file.write('        </pattern>\n')
        svg_file.write('    </defs>\n')
        svg_file.write('    <rect x="0" y="0" width="100%" height="100%" fill="url(#grid_pattern)"/>\n')
        svg_file.write('</svg>\n')


def create_dots(size):
    file_name = "dots_{}.svg".format(size)
    out_dir = "./svg_files/"
    opath = os.path.join(out_dir, file_name)

    with open(opath, "w") as svg_file:
        svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}mm" height="{size}mm" viewBox="0 0 {size} {size}">\n')
        svg_file.write('    <defs>\n')
        svg_file.write('        <pattern id="dots_pattern" width="1mm" height="1mm" patternUnits="userSpaceOnUse">\n')
        svg_file.write('            <circle cx="0.5mm" cy="0.5mm" r="0.5mm" fill="black"/>\n')
        svg_file.write('        </pattern>\n')
        svg_file.write('    </defs>\n')
        svg_file.write('    <rect x="0" y="0" width="100%" height="100%" fill="url(#dots_pattern)"/>\n')
        svg_file.write('</svg>\n')


def create_svg(size, pattern="lines"):
    if pattern == "lines":
        create_lines(size)
    elif pattern == "grid":
        create_grid(size)
    elif pattern == "dots":
        create_dots(size)
    else:
        raise ValueError("Invalid pattern type")

if __name__ == "__main__":
    # size = float(input("Enter the size in mm: "))
    size = [150, 175, 200, 225, 250]
    pattern = ["lines", "grid", "dots"]
    for s in size:
        for p in pattern:
            create_svg(s, p)
    create_svg(size)
