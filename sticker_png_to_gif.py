# encoding=big5
import imageio
import numpy
import sys

SIZE = 288

# ENV
im_name = input("請輸入圖片檔名:")
im = imageio.imread(im_name)
# im=im.astype("int32")
WIDTH_n = int(im.shape[1] // SIZE)
HEIGHT_n = int(im.shape[0] // SIZE)
TOTAL_n = WIDTH_n * HEIGHT_n

# Splitter
im_list = []
for col in range(0, HEIGHT_n):
    for row in range(0, WIDTH_n):
        for times in (0, 1):
            im_list.append(im[col * SIZE:(col + 1) * SIZE, row * SIZE:(row + 1) * SIZE])
imageio.mimwrite(".//complete.gif", im_list, duration=0.02)