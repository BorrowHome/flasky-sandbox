import cv2
import matplotlib
import numpy as np
import pandas as pd
from docx.shared import Mm
from docxtpl import InlineImage

from app.utils.frame.sub import PictureSub

matplotlib.use('Agg')
# python – Matplotlib – Tcl_AsyncDelete：错误的线程删除了异步处理程序？
from matplotlib import pyplot as plt
from sklearn import linear_model

from app.utils.areas_height.divideHeight import divideH
from app.utils.areas_height.divideS import ostu
from app.utils.frame.site import Site
from config import Config


def sand_area_contraction(title, y_axies, file_location='', num_list=[20, 20, 40, 50], color='b'):
    name_list = ['第一区', '第二区', '第三区', '第四区']
    num_list = num_list
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.figsize'] = (8.0, 5.0)

    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.bar(range(len(num_list)), num_list, tick_label=name_list, color=color)
    plt.title(title)
    plt.ylabel(y_axies)
    # plt.xlabel('X axis')
    plt.grid(axis='y')
    plt.savefig(file_location + title + '.png')
    plt.close()

    return file_location + title + '.png'


# 获取线性回归关系 并返回存储的图像关系 y=ax+b
def li_liner_regression(x, y, test_x, name, file_location=''):
    plt.figure()
    print('liner_regression')
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    test_x = np.array(test_x).reshape(-1, 1)
    print('df')
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    print('Coefficients: A= \n', regr.coef_)
    a = regr.coef_
    b = regr.intercept_
    print('Coefficients: B= \n', regr.intercept_)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.figsize'] = (8.0, 5.0)

    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.scatter(x, y, color='black')
    plt.plot(test_x, regr.predict(test_x), color='blue',
             linewidth=3)
    print("title{}".format(name))
    file_name = file_location + name + '.png'
    plt.title(name)
    plt.savefig(file_name)
    plt.close()
    return {'a': a, 'b': b, 'file_name': file_name}


# 计算对应的数据线性回归关系
def get_result(file_location=''):
    document_path = Config.SAVE_DOCUMENT_PATH
    print('开始读取excel')
    data = pd.read_excel(document_path + 'result.xlsx', header=0,
                         names=['pp', 'pf', 'dp', 'ua', 'c', 'w', 'q', 'h', 'fai', 'vcs', 'vpx', 'ueq', 'heq'])
    #  线性回归配置文件
    print(data)
    print('==========' * 20)
    print('读取文件成功')
    data_liner = Config.LINER_CONFIG
    result = {}
    for key in data_liner:
        item = data_liner.get(key)
        print(item)
        title = item.get('title')
        x = list(data.get(item.get('x')).astype(float))
        print(x)
        y = list(data.get(item.get('y')).astype(float))
        print(y)
        result[key] = li_liner_regression(x, y, x[0:len(x):2], title, file_location)

    return result


# 多个曲线放在一个坐标轴里面 生成一张图片 并返回其位置
def li_multiple_plot(length, file_location='', names=[], x_text='', y_text=''):
    if len(names) == 0:
        names = list(range(0, length))
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.figsize'] = (8.0, 5.0)

    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    document_path = Config.SAVE_DOCUMENT_PATH

    for i in range(length):
        csv_data = pd.read_csv(file_location + "sand_" + str(names[i]) + ".csv", header=None, names=['x', 'y'])
        plt.plot(csv_data['x'], csv_data['y'],
                 label='video_' + str(names[i]))

    name = Config.UPLOAD_IMAGE_PATH + 'multiple_lines.png'
    plt.legend()
    plt.ylabel(y_text)
    plt.xlabel(x_text)
    plt.savefig(name)
    plt.close()

    return name


def run_single_image(file_location, tpl, names=[], x_text='', y_text=''):
    result = []
    for i in names:
        single_picture = li_singleLine_plot(file_location, i, x_text, y_text)
        file = InlineImage(tpl,single_picture, Mm(100))
        result.append({
            "video_name": i,
            "file": file
        })
    return result


# 获取单条数据的返回
def li_singleLine_plot(file_location='', name='', x_text='', y_text=''):
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.figsize'] = (8.0, 5.0)

    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率

    csv_data = pd.read_csv(file_location + "sand_" + str(name) + ".csv", header=None, names=['x', 'y'])
    plt.plot(csv_data['x'], csv_data['y'])

    file_name = Config.UPLOAD_IMAGE_PATH + 'plt_{}.png'.format(name)
    plt.legend()
    plt.ylabel(y_text)
    plt.xlabel(x_text)
    plt.savefig(file_name)
    plt.close()

    return file_name


#   获取面积关系
def get_multiple_iback(length, names=[]):
    if len(names) == 0:
        names = list(range(0, length))
    print(names)
    image_path = Config.UPLOAD_IMAGE_PATH
    document_location = Config.SAVE_DOCUMENT_PATH
    results = []
    for id in range(length):
        with open(document_location + "site_" + str(names[id]) + ".txt", "r+") as  f:
            a = f.readlines()
            frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
        path = image_path + "ipaint_{}.png".format(names[id])
        # imread 的filename 长度有限制。
        print(path)
        s = cv2.imread(path.strip())  # ipaint 是直接减去的图像
        print(s)
        sub = PictureSub()
        image_info = sub.iblack(s, 220)  # 图像变为黑白两种
        # image_info = cv.imread(image_locatoion + 'iblack_' + str(names[id]) + '.png')
        result_h = divideH(image_info, frame_location.locate_x, frame_location.locate_y,
                           frame_location.move_x, frame_location.move_y)

        result_a = ostu(image_info, frame_location.locate_x, frame_location.locate_y,
                        frame_location.move_x, frame_location.move_y)
        results.append(
            {
                "area": result_a,
                "height": result_h
            }
        )
    return results


if __name__ == '__main__':
    document_path = Config.SAVE_DOCUMENT_PATH

    # li_multiple_plot(3, document_path)
    # result = li_liner_regression([1, 2, 3, 4, 5], [5, 8, 11, 14, 17], [2, 3, 4], "name")
    data = pd.read_excel('result.xlsx', header=0,
                         names=['pp', 'pf', 'dp', 'ua', 'c', 'w', 'q', 'h', 'fai', 'vcs', 'vpx', 'ueq', 'heq'])
    print(data)
