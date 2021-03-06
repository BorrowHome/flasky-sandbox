#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2


# from PIL import Image

# INFO 2020/6/12 16:12 liliangbin  获取砂子的面积
############################################二值化砂子像素统计
def ostu(img):
    area = 0
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转灰度
    blur = cv2.GaussianBlur(image, (5, 5), 0)  # 阈值一定要设为 0 ！高斯模糊
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 二值化 0 = black ; 1 = white
    # cv2.namedWindow("image", cv2.WINDOW_FREERATIO)
    # cv2.imshow('image', th3)
    a = cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print a
    height, width = th3.shape
    for i in range(height):
        for j in range(width):
            if th3[i, j] == 0:
                area += 1
    print("done")
    return area


if __name__ == '__main__':
    src = cv2.imread("chun.png")
    area = ostu(src)
    print(area)
