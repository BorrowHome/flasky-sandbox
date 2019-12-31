##############################红色矩形框顶点坐标                                                                                                                                                                                     顶点坐标
import cv2 as cv


class PictureSub(object):
    def __init__(self):
        pass

    def __int__(self, first_frames, current_frames):
        self.first_frames = first_frames
        self.current_frames = current_frames

    def left_up(self, image):
        shape = image.shape
        print("height", shape[0])
        print("width", shape[1])
        print("left_up:")
        # x=0
        # y=0
        list1 = []
        list2 = []
        for i in range(shape[1]):
            for j in range(shape[0]):
                if (image[j, i, 0] < 60 and image[j, i, 1] < 60 and image[j, i, 2] > 230):
                    list1.append(i)
                    list2.append(j)

                    break

        res = {
            "list_x": list1[0],
            "list_y": list2[0],
        }
        print(list1[0], list2[0])
        # print(list1[-1], list2[-1])
        # print(list2[0])
        return res

    def right_up(self, image):
        shape = image.shape
        # print(shape[0])
        # print(shape[1])
        print("right_up:")
        # x=0
        # y=0
        list1 = []
        list2 = []
        for i in range(shape[1]):
            for j in range(shape[0]):
                if (image[j, i, 0] < 60 and image[j, i, 1] < 60 and image[j, i, 2] > 230):
                    list1.append(i)
                    list2.append(j)

                    break

        res = {
            "list_x": list1[-1],
            "list_y": list2[-1],
        }
        # print(list1[0],list2[0])
        print(list1[-1], list2[-1])
        # print(list2[0])
        return res

    def left_down(self, image):
        shape = image.shape
        # print(shape[0])
        # print(shape[1])
        print("left_down")
        # x=0
        # y=0
        list1 = []
        list2 = []
        for i in range(shape[1] - 1, 0, -1):
            for j in range(shape[0] - 1, 0, -1):
                if (image[j, i, 0] < 60 and image[j, i, 1] < 60 and image[j, i, 2] > 170):
                    list1.append(i)
                    list2.append(j)

                    break

        res = {
            "list_x": list1[-1],
            "list_y": list2[-1],
        }
        # print(list1[0], list2[0])
        print(list1[-1], list2[-1])
        # print(list2[0])
        return res

    def right_down(self, image):
        shape = image.shape
        # print(shape[0])
        # print(shape[1])
        print("right_down")
        # x=0
        # y=0
        list1 = []
        list2 = []
        for i in range(shape[1] - 1, 0, -1):
            for j in range(shape[0] - 1, 0, -1):
                if (image[j, i, 0] < 60 and image[j, i, 1] < 60 and image[j, i, 2] > 170):
                    list1.append(i)
                    list2.append(j)

                    break

        res = {
            "list_x": list1[0],
            "list_y": list2[0],
        }
        print(list1[0], list2[0])
        # print(list1[-1], list2[-1])
        # print(list2[0])
        return res


if __name__ == '__main__':
    sub = PictureSub()
    src1 = cv.imread('red.png')
    sub.left_up(src1)
    sub.right_up(src1)
    sub.left_down(src1)
    sub.right_down(src1)
