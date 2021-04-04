# """author: liliangbin create at 2019-10-1 @No longer used"""
import csv

import cv2 as cv
from PIL import Image

from config import Config
import numpy as np
import cv2


class PictureSub(object):
    def __init__(self):
        pass

    def testf(self, path1, path2, name):
        imageA = Image.open(path1)  # 导入图片
        imageB = Image.open(path2)

        grayA = imageA.convert('L')  # 转为灰阶
        grayB = imageB.convert('L')

        width_A, height_A = grayA.size  # 设置图片长宽，截取图片，肯定grayA的尺寸=grayB的尺寸

        data_c = np.zeros(shape=(width_A, height_A))  # 初始化矩阵data_c

        for i in range(1, width_A):  # 例遍横坐标，建立矩阵  需注意，列表首位是0.numpy首位是1，Image首位按1,
            for j in range(1, height_A):  # 例遍纵坐标
                im_data_1 = grayA.getpixel((i, j))  # 原始图片像素灰阶数值
                im_data_2 = grayB.getpixel((i, j))  # 当前图片像素灰阶数值
                im_data = (im_data_1 - im_data_2)  # 两个图片像素灰阶数值差
                ima_data = abs(im_data)
                if ima_data < 15:  # 以2为阙值，灰阶值差异大于2及沙砾，小于2按照光线影响
                    data_c[i, j] = 225  # 建立矩阵data_c
                else:
                    data_c[i, j] = 0
        data_c = data_c.T
        cv2.imwrite(Config.UPLOAD_IMAGE_PATH + "ipaint_" + name + ".png", data_c)
        return data_c

    def __int__(self, first_frames, current_frames):
        self.first_frames = first_frames
        self.current_frames = current_frames

    #     get the video first frames

    def subtract_demo(self, m1, m2):  # 像素的减运算
        dst = m2
        img_hsv = cv.cvtColor(dst, cv.COLOR_BGR2HSV)
        red_min = np.array([0, 50, 50])
        red_max = np.array([30, 255, 255])
        red_mask = cv.inRange(img_hsv, red_min, red_max)
        img_red = cv.bitwise_and(dst, dst, mask=red_mask)
        return img_red

    def inverse(self, image):
        shape = image.shape
        channels = shape[2]
        # for cn in range(channels):
        #     """255-原本的颜色就变成了反色"""
        #     image[:, :, cn] = 255 - image[:, :, cn]
        # # cv.imshow("imshow_inverse", image)
        return image

    def iblack(self, image, k):
        shape = image.shape
        print(shape)
        channels = shape[2]
        # for cn in range(channels):
        #     """255-原本的颜色就变成了反色"""
        #     for i in range(shape[0]):
        #         for j in range(shape[1]):
        #             # 二向化归一
        #             if (image[i, j, cn] < k):
        #                 image[i, j, cn] = 0

        return image

    # k 是一个阈值
    def ipaint(self, image, k, name, locate_x, move_x, locate_y, move_y):
        document_path = Config.SAVE_DOCUMENT_PATH
        list1 = []
        list2 = []
        bottom_x = move_x + locate_x
        bottom_y = move_y + locate_y
        with open(document_path + "sand_" + name + ".csv", "w", newline="")as f:
            writer = csv.writer(f)
            for i in range(locate_x, locate_x + move_x, 1):
                flag = True
                for j in range(locate_y, move_y + locate_y, 1):
                    if (image[j, i,2] > 10):
                        # with open(r"E:sand.csv", "w", newline="")as f:
                        #  writer = csv.writer(f)
                        x = i - locate_x
                        y = bottom_y - j
                        writer.writerow([x, y])
                        list1.append(x)
                        list2.append(y)
                        flag = False
                        break
                    # m = m + 1
                if flag:
                    writer.writerow([i - locate_x, 0])
                    list1.append(i - locate_x)
                    list2.append(0)

        res = {
            "list_x": list1,
            "list_y": list2
        }

        return res


if __name__ == '__main__':
    pass
