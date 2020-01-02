#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from PIL import Image


#################################3矩形框像素统计
def get_frame_area(locate_x, locate_y, end_x, end_y):
    area = 0
    print(locate_y,end_y)
    for i in range(locate_x, end_x, 1):
        for j in range(locate_y, end_y, 1):
            print("doone")
            area = area + 1
    print(area)
    return area
