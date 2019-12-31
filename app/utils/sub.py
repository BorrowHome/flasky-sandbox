# """author: liliangbin create at 2019-10-1 @No longer used"""
import csv

import cv2 as cv

class PictureSub(object):
    def __init__(self):
        pass

    def __int__(self, first_frames, current_frames):
        self.first_frames = first_frames
        self.current_frames = current_frames

    #     get the video first frames

    def subtract_demo(self,m1, m2):  # 像素的减运算
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

    def iblack(self,image, k):
        shape = image.shape
        channels = shape[2]
        for cn in range(channels):
            """255-原本的颜色就变成了反色"""
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if (image[i, j, cn] < k):
                        image[i, j, cn] = 0



        return image

    def ipaint( self,image, k):
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
                        writer.writerow([i - 0, j - 0])
                        list1.append(i - 0)
                        list2.append(j - 0)
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

                        break

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
 src1 = cv.imread('E:firstFrame5.jpg')
 src2 = cv.imread('E:/back3/888.jpg')
 q = sub.subtract_demo(src1, src2)
 cv.imwrite('E:/back4/666.jpg', q)
 s = sub.inverse(q)
 cv.imwrite('E:/back4/777.jpg', s)
 t =sub.iblack(s, 210)
 # s = sub.isblack(t, 240)
 cv.imwrite('E:/back4/8.jpg', t)
 # 把数据给写入到csv文件里面
 sub.ipaint(t, 50)

# m = cv.rectangle(s, (170, 450), (1450, 960), (0, 0, 255), 3)
 cv.imwrite('E:/back4/9.jpg', s)
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
