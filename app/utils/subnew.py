import csv

import cv2 as cv
import numpy as np


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
        channels = shape[2]
        for cn in range(channels):
            """255-原本的颜色就变成了反色"""
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if (image[i, j, cn] < k):
                        image[i, j, cn] = 0
                        if i > 120 or i < 248 or j < 430 or j > 48:
                            image[i, j, 0] = 0
                            image[i, j, 1] = 0
                            image[i, j, 2] = 0
                    if i > 244 or i < 160 or j > 430 or j < 48:
                        image[i, j, 0] = 255
                        image[i, j, 1] = 255
                        image[i, j, 2] = 255

        return image

    def ipaint(self, image, k):
        shape = image.shape
        print(shape[0])
        print(shape[1])
        list1 = []
        list2 = []
        with open("sand.csv", "w", newline="")as f:
            writer = csv.writer(f)
            for i in range(shape[1]):
                for j in range(shape[0]):
                    if (image[j, i, 2] < k):
                        # with open(r"E:sand.csv", "w", newline="")as f:
                        #  writer = csv.writer(f)
                        writer.writerow([i, j])
                        list1.append(i)
                        list2.append(j)
                        # sheet.write(m, 1, j -450)
                        image[j + 1, i, 1] = 255
                        image[j + 2, i, 1] = 255
                        image[j + 3, i, 1] = 255
                        image[j + 1, i, 0] = 0
                        image[j + 2, i, 0] = 0
                        image[j + 3, i, 1] = 0
                        image[j + 1, i, 2] = 0
                        image[j + 2, i, 2] = 0
                        image[j + 3, i, 2] = 0
                        # m = m + 1
                        if (i < 150):
                            for l in range(j + 4, 244):
                                image[l, i, 0] = 0
                                image[l, i, 1] = 0
                                image[l, i, 2] = 0
                        break

        # array_list_y = np.array(list2)
        # array_list_y_fit = signal.medfilt(array_list_y, 3)
        # list2 = array_list_y_fit.tolist()
        #
        with open('test.txt', 'w') as  f:
            f.write(str(list2))

        head = list1[0]
        print("head === > ", head)
        y_zeros = np.ones(head) * 244
        print(head)
        list_x_add = range(0, head)
        print("len  head == > ", list_x_add)
        print(list_x_add)
        print("list X ", list_x_add)
        list1 = list(list_x_add) + list1

        list2 = y_zeros.tolist() + list2
        print(len(list1), "  == list2 === >", len(list2))

        list1 = list1[50:]
        list2 = list2[50:]
        res = {
            "list_x": list1,
            "list_y": list2
        }
        print(list1)
        print(list2)
        return res

    def test_done(self):
        print(" done ")


if __name__ == '__main__':
    sub = PictureSub()
    src1 = cv.imread('back.png')
    print(src1.shape)
    src2 = cv.imread('test2.png')
    q = sub.subtract_demo(src1, src2)
    s = sub.inverse(q)
    t = sub.iblack(s, 210)
    # s = sub.isblack(t, 240)

    # 把数据给写入到csv文件里面
    sub.ipaint(t, 50)

    # m = cv.rectangle(s, (170, 450), (1450, 960), (0, 0, 255), 3)
    cv.imwrite('write.jpg', s)

    # dirr ='F:/frame/'
    # filelist = os.listdir(dirr)
    # for item in filelist:
    #     src2 = cv.imread(dirr+item)
    #     q=subtract_demo(src1, src2)
    #     s =inverse(q)
    #     t=iblack(q,20)
    #     #cv.GaussianBlur(t, (3, 3), 0)
    #     iblack(t,220)
    #    # cv.cvtColor(t, cv.COLOR_BGR2GRAY)
    #     m = cv.rectangle(t,(170,450),(1450,960),(0,0,255),3)
    #     # name = 'pic/'+'00'+str(i)+'.jpg'
    #     cv.imwrite('E:/frame10/'+item, m)
    # cv.imshow("subtract_demo", q)

    cv.destroyAllWindows()
