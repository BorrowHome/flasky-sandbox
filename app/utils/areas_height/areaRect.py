#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from PIL import Image

# INFO 2020/6/12 16:10 liliangbin  根据边框大小，计算像素点的面积    ？？？这个地方可以直接乘计吧。author===> 赵欣
#################################3矩形框像素统计
def get_frame_area(locate_x, locate_y, end_x, end_y):
    area = 0
    print(locate_y,end_y)
    for i in range(locate_x, end_x, 1):
        for j in range(locate_y, end_y, 1):
            area = area + 1
    print(area)
    return area
