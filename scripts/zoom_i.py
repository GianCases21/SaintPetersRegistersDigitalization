import sys
from PIL import Image, ImageEnhance

# usage: python3 zoom_i.py "PAGE 8-9.JPG" X1 Y1 X2 Y2 out.jpg
base = "/workspace/drive_sample/Registers/cemetary_plots/Cemetary Plots/1847/"
name, x1, y1, x2, y2, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
im = Image.open(base + name)
c = im.crop((x1, y1, x2, y2))
c = ImageEnhance.Contrast(c).enhance(1.6)
c = ImageEnhance.Brightness(c).enhance(1.3)
c.thumbnail((1400, 1400))
c.save(out, quality=90)
print(out, c.size)
