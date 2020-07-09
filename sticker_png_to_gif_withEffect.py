# encoding=big5
import imageio
import numpy
import sys
# filename=sys.argv[1]

SIZE = 288

"""
class SHAFT:
    x = numpy.array([64, 0, 0, 0])
    y = numpy.array([0, 64, 0, 0])
    z = numpy.array([0, 0, 64, 0])
"""

# ENV
im_name = input("請輸入圖片檔名:")
im = imageio.imread(im_name)
# im=im.astype("int32")
WIDTH_n = int(im.shape[1] // SIZE)
HEIGHT_n = int(im.shape[0] // SIZE)
TOTAL_n = WIDTH_n * HEIGHT_n

SHAFT = []
SHAFT.append(numpy.array([0, 0, 0, 0]))
x = numpy.around(TOTAL_n / 3)
y = numpy.around(TOTAL_n / 3 * 2) - x
z = TOTAL_n - numpy.around(TOTAL_n / 3 * 2)
x_array = numpy.array([256 / x, 0, 0, 0])
y_array = numpy.array([0, 256 / y, 0, 0])
z_array = numpy.array([0, 0, 256 / z, 0])
for i in range(1, TOTAL_n):
    if (i >= 1 and i <= y):
        SHAFT.append(SHAFT[i - 1] + y_array)
    elif (i > y and i <= x + y):
        SHAFT.append(SHAFT[i - 1] + x_array)
    elif (i > x + y and i <= x + y + z):
        SHAFT.append(SHAFT[i - 1] + z_array)
for i in range(0, len(SHAFT)):
    SHAFT[i] = numpy.around(SHAFT[i])
    SHAFT.append(SHAFT[i])
"""
SHAFT=[
    numpy.array([0, 0, 0, 0]),
    numpy.array([0, 63, 0, 0]),
    numpy.array([0, 127, 0, 0]),
    numpy.array([0, 191, 0, 0]),
    numpy.array([0, 255, 0, 0]),
    numpy.array([63, 255, 0, 0]),
    numpy.array([127, 255, 0, 0]),
    numpy.array([191, 255, 0, 0]),
    numpy.array([255, 255, 0, 0]),
    numpy.array([255, 255, 63, 0]),
    numpy.array([255, 255, 127, 0]),
    numpy.array([255, 255, 191, 0]),
    numpy.array([0, 0, 0, 0]),
    numpy.array([0, 63, 0, 0]),
    numpy.array([0, 127, 0, 0]),
    numpy.array([0, 191, 0, 0]),
    numpy.array([0, 255, 0, 0]),
    numpy.array([63, 255, 0, 0]),
    numpy.array([127, 255, 0, 0]),
    numpy.array([191, 255, 0, 0]),
    numpy.array([255, 255, 0, 0]),
    numpy.array([255, 255, 63, 0]),
    numpy.array([255, 255, 127, 0]),
    numpy.array([255, 255, 191, 0]),
]
"""

# Splitter
im_list = []
for col in range(0, HEIGHT_n):
    for row in range(0, WIDTH_n):
        for times in (0, 1):
            im_list.append(im[col * SIZE:(col + 1) * SIZE, row * SIZE:(row + 1) * SIZE])
for i in range(0, len(im_list)):
    name = ".//temp//%d.png" % (i)
    imageio.imwrite(name, im_list[i])
    im_list[i] = im_list[i].astype("int32")

# gray-scale
from PIL import Image

im_list_LA_B = []
im_list_LA_W = []
for i in range(0, len(im_list)):
    img = Image.open(".//temp//%d.png" % (i)).convert('LA')
    img.save(".//temp//%d_gray.png" % (i))
    # disassemble
    im_list_LA_B.append(imageio.imread(".//temp//%d_gray.png" % (i)))
    im_list_LA_B[i] = numpy.where(im_list_LA_B[i] < 100, im_list_LA_B[i], 255)
    im_list_LA_W.append(imageio.imread(".//temp//%d_gray.png" % (i)))
    im_list_LA_W[i] = numpy.where(im_list_LA_W[i] > 250, im_list_LA_B[i], 0)
    # imageio.imwrite(".//temp//%d_gray_pick.png"%(i), im_list_LA_B[i])

# color_shaft
im_list_coshaft = []

for i in range(0, len(im_list) - TOTAL_n):
    im_list_coshaft.append(im_list[i] + SHAFT[i])
    im_list_coshaft[i] = numpy.where(im_list_coshaft[i] >= 256, 512 - im_list_coshaft[i], im_list_coshaft[i])
    im_list_coshaft[i] = numpy.where(im_list_coshaft[i] == 256, 255, im_list_coshaft[i])
    # imageio.imwrite(".//temp//%d_coshaft.png" % (i), im_list_coshaft[i])
for i in range(len(im_list) - TOTAL_n, len(im_list)):
    neg = numpy.array([256, 256, 256, 0]) + im_list[i]
    im_list_coshaft.append(numpy.where(neg >= 256, 512 - neg, neg) + SHAFT[i])
    im_list_coshaft[i] = numpy.where(im_list_coshaft[i] >= 256, 512 - im_list_coshaft[i], im_list_coshaft[i])
    im_list_coshaft[i] = numpy.where(im_list_coshaft[i] == 256, 255, im_list_coshaft[i])
    # imageio.imwrite(".//temp//%d_coshaft.png" % (i), im_list_coshaft[i])

# merge
for i in range(0, len(im_list)):
    im_list_coshaft[i] = numpy.where(im_list_LA_B[i] < 100, im_list_LA_B[i], im_list_coshaft[i])
    im_list_coshaft[i] = numpy.where(im_list_LA_W[i] == 255, 255, im_list_coshaft[i])
    im_list_coshaft[i] = im_list_coshaft[i].astype("uint8")
    imageio.imwrite(".//pre//%d.png" % (i), im_list_coshaft[i])
"""
for i in range(0,2):
    im_list_coshaft.append(im_list[i] + SHAFT.y*i)
    im_list_coshaft[i]=numpy.where(im_list_coshaft[i]>256,512-im_list_coshaft[i],im_list_coshaft[i])
    imageio.imwrite(".//temp//%d_coshaft.png" % (i), im_list_coshaft[i])
"""

imageio.mimwrite(".//complete.gif", im_list_coshaft, fps=60)
import os
PATH = os.path.abspath('.') + "\\"
os.startfile(PATH+"complete.gif")
