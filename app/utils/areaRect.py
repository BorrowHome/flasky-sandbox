#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from PIL import Image

area = 0


#################################3矩形框像素统计
def get_frame_area(locate_x, locate_y, move_x, move_y):
    global area
    for i in range(locate_x, move_x):
        for j in range(locate_y, move_y):
            area += 1
    print(area)
    return area
