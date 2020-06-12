#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

from config import Config


# from PIL import Image
# INFO 2020/6/12 16:14 liliangbin  文档生成时使用，沙子面积分

############################################二值化沙子像素统计
def ostu(img, locate_x, locate_y, move_x, move_y):
    area1 = 0
    area2 = 0
    area3 = 0
    area4 = 0

    left = locate_x
    right = locate_x + move_x
    width = move_x
    height = move_y + locate_y
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转灰度
    blur = cv2.GaussianBlur(image, (5, 5), 0)  # 阈值一定要设为 0 ！高斯模糊
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 二值化 0 = black ; 1 = white
    # cv2.namedWindow("image", cv2.WINDOW_FREERATIO)
    # cv2.imshow('image', th3)
    a = cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print a
    # height, width = th3.shape
    one_four = int(width / 4)
    ####first area
    for i in range(height):
        for j in range(left, left + one_four):
            if th3[i, j] == 0:
                area1 += 1
    print("frist_area")
    print(area1)
    #####second area
    for i in range(height):
        for j in range(left + one_four, left + one_four * 2):
            if th3[i, j] == 0:
                area2 += 1
    print("second_area")
    print(area2)
    #####third area
    for i in range(height):
        for j in range(left + one_four * 2, left + one_four * 3):
            if th3[i, j] == 0:
                area3 += 1
    print("third_area")
    print(area3)
    #####forth area
    for i in range(height):
        for j in range(left + one_four * 3, right):
            if th3[i, j] == 0:
                area4 += 1
    print("forth_area")
    print(area4)
    print("###")
    averageS = (area1 + area2 + area3 + area4) / 4

    #####求增幅
    print("#####")

    first_second = li_utils(area1, area2)
    first_second = "%.2f%%" % (first_second * 100)
    print("first_second:", first_second)

    second_third = li_utils(area2, area3)
    second_third = "%.2f%%" % (second_third * 100)
    print("second_third:", second_third)

    third_forth = li_utils(area3, area4)
    third_forth = "%.2f%%" % (third_forth * 100)
    print("third_forth:", third_forth)


    averageS = round(averageS, 2)
    print("averageS:", averageS)
    added = [first_second, second_third, third_forth]
    averageArea = averageS
    areas = [area1, area2, area3, area4]
    return {
        'areas': areas,
        'added': added,
        'averageArea': averageArea,
    }


def li_utils(first, second):
    if first == 0:
        return 0
    else:
        result = (second - first) / first
        return result


if __name__ == '__main__':
    src1 = cv2.imread(Config.UPLOAD_IMAGE_PATH + "iblack_2.png")  ###该图片为经过函数iblack 后的黑白图片
    result = ostu(src1, 2, 66, 609, 54)
    print(result)
    #     #2 66 609  54
