import os
import PIL.Image as Image
import cv2
import numpy as np
from config import Config
# image_path = r'C:\Users\admin\Desktop\沙箱截图\\'  # 图片集的地址
# image_save_path = r'C:\Users\admin\Desktop\kk\final.jpg'  # 图片合并后的保存地址
#
# image_path = r"D:\kk\a.jpg"
# coordinate_path = r"D:\kk\coordinate.txt"
# save_path = "D://kk//"

def image_crop(image_path,coordinate_path,save_path):  #图片裁减，参数分别为背景图文件路径，坐标文件路径，裁剪后图片保存路径
    img = cv2.imread(image_path)
    f = open(coordinate_path, "r")
    line = f.read()
    num = line.split('\n')   #读取坐标
    print(num[0], num[1], num[2], num[3])
    locate_x, locate_y, move_x, move_y =num[0], num[1], num[2], num[3]
    final_y = int(locate_y) + int(move_y)
    final_x = int(locate_x) + int(move_x)
    # print(final_y,final_x)
    crop = img[int(locate_y):int(final_y),int(locate_x):int(final_x)]  #按照坐标进行裁剪
    # cv2.imshow("image", crop)
    # cv2.waitKey(0)
    cv2.imwrite(save_path + "_mosaic.jpg", crop)   #保存图片


def image_split(image_path,image_names,image_column):  #图片合并算法
    IMAGES_PATH = image_path
    IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
    IMAGE_SIZE = 256  # 每张小图片的大小
    IMAGE_ROW = 1  # 图片间隔，也就是合并成一张图后，一共有几行
    IMAGE_COLUMN = image_column  # 图片间隔，也就是合并成一张图后，一共有几列
    IMAGE_SAVE_PATH = Config.UPLOAD_IMAGE_PATH+'VideoMosaic.png'

    # 获取图片集地址下的所有图片名称
    print(image_names)
    image_names0 = [name for name in image_names]
    image_names = image_names0[:image_column]  # 取文件夹中前n张截图(假设image_column即需要合并的图片数量为n）

    print("image_names", image_names)
    # 简单的对于参数的设定和实际图片集的大小进行数量判断
    if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
        raise ValueError("合成图片的参数和要求的数量不能匹配！")

    # 定义图像拼接函数
    def image_compose():
        to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        for y in range(1, IMAGE_ROW + 1):
            for x in range(1, IMAGE_COLUMN + 1):
                from_image = Image.open(image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                    (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
                to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
        return to_image.save(IMAGE_SAVE_PATH)  # 保存新图

    image_compose()  # 调用拼接函数