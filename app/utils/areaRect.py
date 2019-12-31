#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

# from PIL import Image

area = 0


#################################3矩形框像素统计
def ostu(img):
    global area
    # image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转灰度
    # blur = cv2.GaussianBlur(image, (5, 5), 0)  # 阈值一定要设为 0 ！高斯模糊
    # ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 二值化 0 = black ; 1 = white
    # cv2.namedWindow("image", cv2.WINDOW_FREERATIO)
    # cv2.imshow('image', img)
    # a = cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print a
    # height, width = th3.shape
    for i in range(450, 960):
        for j in range(190, 1415):
            area += 1
    print(area)
    return area


src1 = cv2.imread("firstFrame1.jpg")
ostu(src1)
