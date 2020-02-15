#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
#from PIL import Image

area1= 0
area2 = 0
area3 = 0
area4 = 0
############################################二值化沙子像素统计
def ostu(img,left,right,width,height):
    global area1,area2,area3,area4


    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转灰度
    blur = cv2.GaussianBlur(image, (5, 5), 0)  # 阈值一定要设为 0 ！高斯模糊
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 二值化 0 = black ; 1 = white
   # cv2.namedWindow("image", cv2.WINDOW_FREERATIO)
   # cv2.imshow('image', th3)
    a = cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print a
    #height, width = th3.shape
    one_four=int(width/4)
    ####first area
    for i in range(height):
        for j in range(left,left+one_four):
            if th3[i, j] == 0:
                area1 += 1
    print("frist_area")
    print(area1)
    #####second area
    for i in range(height):
        for j in range(left+one_four,left+one_four*2):
            if th3[i, j] == 0:
                area2 += 1
    print("second_area")
    print(area2)
    #####third area
    for i in range(height):
        for j in range(left+one_four*2, left+one_four*3):
            if th3[i, j] == 0:
                area3 += 1
    print("third_area")
    print(area3)
    #####forth area
    for i in range(height):
        for j in range(left+one_four*3, right):
            if th3[i, j] == 0:
                area4 += 1
    print("forth_area")
    print(area4)
    print("###")
    averageS=(area1+area2+area3+area4)/4
    averageS=round(averageS,2)
    print("averageS:",averageS)
src1 = cv2.imread("E:/back4/6.jpg")###该图片为经过函数iblack 后的黑白图片
ostu(src1,8,480,472,352)
