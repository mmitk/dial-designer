from PIL import Image
import PIL.ImageOps
import sys

in_image = sys.argv[1]
out_image = sys.argv[2]

image = Image.open(in_image)

inverted_image = PIL.ImageOps.invert(image)

inverted_image.save(out_image)