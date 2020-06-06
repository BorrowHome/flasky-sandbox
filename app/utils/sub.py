# """author: liliangbin create at 2019-10-1 @No longer used"""
import csv

import cv2 as cv

from config import Config


class PictureSub(object):
    def __init__(self):
        pass

    def __int__(self, first_frames, current_frames):
        self.first_frames = first_frames
        self.current_frames = current_frames

    #     get the video first frames

    def subtract_demo(self, m1, m2):  # 像素的减运算
        dst = cv.subtract(m1, m2)
        # cv.imshow("subtract_demo", dst)
        return dst

    def inverse(self, image):
        shape = image.shape
        channels = shape[2]
        for cn in range(channels):
            """255-原本的颜色就变成了反色"""
            image[:, :, cn] = 255 - image[:, :, cn]
        # cv.imshow("imshow_inverse", image)
        return image

    def iblack(self, image, k):
        shape = image.shape
        print(shape)
        channels = shape[2]
        for cn in range(channels):
            """255-原本的颜色就变成了反色"""
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if (image[i, j, cn] < k):
                        image[i, j, cn] = 0

        return image

    def ipaint(self, image, k, id, locate_x, move_x, locate_y, move_y):
        image_path = Config.UPLOAD_IMAGE_PATH
        document_path = Config.SAVE_DOCUMENT_PATH
        shape = image.shape
        print(shape[0]) # 480  高度
        print(shape[1]) # 640  宽度
        list1 = []
        list2 = []
        with open(document_path + "sand_" + id + ".csv", "w", newline="")as f:
            writer = csv.writer(f)
            for i in range(locate_x, locate_x + move_x, 1):
                flag = True
                for j in range(locate_y, move_y + locate_y, 1):
                    if (image[j, i, 2] < k):
                        # with open(r"E:sand.csv", "w", newline="")as f:
                        #  writer = csv.writer(f)
                        writer.writerow([i - 0, j - 0])
                        list1.append(i - 0)
                        list2.append(j - 0)
                        flag = False
                        break
                    # m = m + 1
                if flag:
                    writer.writerow([i, locate_y + move_y])
                    list1.append(i)
                    list2.append(locate_y + move_y)

        res = {
            "list_x": list1,
            "list_y": list2
        }

        return res


if __name__ == '__main__':
    pass
