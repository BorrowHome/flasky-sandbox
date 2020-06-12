import cv2

from config import Config

# INFO 2020/6/12 16:13 liliangbin  在文档生成的时候使用。将图像分为4块
def divideH(image, locate_x, locate_y, move_x, move_y):
    # shape = image.shape
    left = locate_x
    right = locate_x + move_x
    down = move_y + locate_y
    width = move_x
    height = move_y + locate_y
    print(left, right, down, height, width)
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    average1 = 0
    average2 = 0
    average3 = 0
    average4 = 0
    first_second = 0

    one_four = int(width / 4)
    for i in range(left, left + one_four):
        for j in range(height):
            if (image[j, i, 2] < 50):
                # with open(r"E:sand.csv", "w", newline="")as f:
                #  writer = csv.writer(f)
                list1.append(down - j)
                # sheet.write(m, 1, j -450)
                break

    # print(list1)
    # print(list1)
    average1 = ave(list1)
    print("first_Height:", average1)
    for i in range(left + one_four, left + one_four * 2):
        for j in range(height):
            if (image[j, i, 2] < 50):
                # with open(r"E:sand.csv", "w", newline="")as f:
                #  writer = csv.writer(f)
                list2.append(down - j)
                # sheet.write(m, 1, j -450)
                break

    # print(list1)
    # print(list2)
    average2 = ave(list2)
    print("second_Height:", average2)
    for i in range(left + one_four * 2, left + one_four * 3):
        for j in range(height):
            if (image[j, i, 2] < 50):
                # with open(r"E:sand.csv", "w", newline="")as f:
                #  writer = csv.writer(f)
                list3.append(down - j)
                # sheet.write(m, 1, j -450)
                break

    # print(list3)
    average3 = ave(list3)
    print("third_Height:", average3)
    for i in range(left + one_four * 3, right):
        for j in range(height):
            if (image[j, i, 2] < 50):
                # with open(r"E:sand.csv", "w", newline="")as f:
                #  writer = csv.writer(f)
                list4.append(down - j)
                # sheet.write(m, 1, j -450)
                break

    # print(list4)
    average4 = ave(list4)
    print("forth_Height:", average4)

    #####求增幅
    print("#####")
    if average1 != 0:
        first_second = (average2 - average1) / average1
    else:
        first_second = 0

    first_second = "%.2f%%" % (first_second * 100)
    print("first_second:", first_second)
    if average2 != 0:
        second_third = (average3 - average2) / average2
    else:
        second_third = 0
    second_third = "%.2f%%" % (second_third * 100)
    print("second_third:", second_third)
    if average3 != 0:

        third_forth = (average4 - average3) / average3
    else:
        third_forth = 0

    third_forth = "%.2f%%" % (third_forth * 100)
    print("third_forth:", third_forth)

    #####求高度平均值
    aveH = (average1 + average2 + average3 + average4) / 4
    aveH = round(aveH, 2)

    print("####")
    print("averageHeight:", aveH)

    hei = [average1, average2, average3, average4]
    added = [first_second, second_third, third_forth]
    averageHeight = aveH
    return {
        'heights': hei,
        'added': added,
        'averageHeight': averageHeight
    }


def ave(list):
    b = len(list)
    if (b == 0):
        return 0
    sum = 0
    for i in list:
        sum = sum + i
    ave = round(sum / b, 2)
    return ave


if __name__ == '__main__':
    file_location = Config.UPLOAD_IMAGE_PATH
    src1 = cv2.imread(file_location + 'iblack_2.png')  ###该图片为经过函数iblack 后的黑白图片
    result = divideH(src1, 2, 66, 609, 54)
    # 2 66 609  54
    print(result)
#     161
# 508
# 1121
# 347
# 58
# 403
# 1267
# 393
