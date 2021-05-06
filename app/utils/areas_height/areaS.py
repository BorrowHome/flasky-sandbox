#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

# from PIL import Image

# INFO 2020/6/12 16:12 liliangbin  获取砂子的面积
############################################二值化砂子像素统计
from app.utils.areas_height.areaRect import get_frame_area
from app.utils.frame.site import Site


def ostu(img, x_start=0, x_end=0, y_start=0, y_end=0):
    area = 0
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转灰度
    blur = cv2.GaussianBlur(image, (5, 5), 0)  # 阈值一定要设为 0 ！高斯模糊
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 二值化 0 = black ; 1 = white
    cv2.imwrite('fsdfs.png', th3)
    height, width = th3.shape
    print(th3.shape)
    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            if th3[j, i] >= 220:
                area += 1
    print("done")
    return area


if __name__ == '__main__':
    src = cv2.imread(r"C:\Users\llb\Documents\coding\test\flasky-sandbox\app\static\image\ipaint_234.png")

    path = r"C:\Users\llb\Documents\coding\test\flasky-sandbox\app\static\document\site_234.txt"
    with open(path, "r+") as f:
        a = f.readlines()
        print(a)
        frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
    frame_area = get_frame_area(frame_location.locate_x,
                                frame_location.locate_y,
                                frame_location.locate_x + frame_location.move_x,
                                frame_location.locate_y + frame_location.move_y)

    print('frame arsea =={}'.format(frame_area))

    area = ostu(src, frame_location.locate_x,
                frame_location.locate_x + frame_location.move_x,
                frame_location.locate_y,
                frame_location.locate_y + frame_location.move_y)
    print(' arsea =={}'.format(area))
