import cv2 as cv
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
# python – Matplotlib – Tcl_AsyncDelete：错误的线程删除了异步处理程序？
from matplotlib import pyplot as plt
from sklearn import linear_model

from app.utils.divideHeight import divideH
from app.utils.divideS import ostu
from app.utils.site import Site
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


def li_liner_regression(x, y, test_x, name, file_location=''):
    print(x)
    print(test_x)
    print(y)
    plt.figure()
    print('liner_regression')
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    test_x = np.array(test_x).reshape(-1, 1)

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
    file_name = file_location + name + '.png'
    plt.title(name)
    plt.savefig(file_name)
    plt.close()
    return {'a': a, 'b': b, 'file_name': file_name}


def get_result(ites, file_location=''):
    vx = []
    vy = []
    scale = []
    v = []
    density = []
    viscosity = []
    for item in ites:
        vx.append(item['vx'])
        vy.append(item['vy'])
        scale.append(item['scale'])
        v.append(item['v'])
        density.append(item['density'])
        viscosity.append(item['viscosity'])
    names = ['流速与水平速度关系回归式', '流速与垂直速度关系回归式',
             '砂比与水平速度关系回归式', '砂比与垂直速度关系回归式',
             '支撑剂密度与水平速度关系回归式', '支撑剂密度与垂直速度关系回归式',
             '压裂液粘度与水平速度关系回归式', '压裂液粘度与垂直速度关系回归式']

    result = {}
    result['v_vx'] = li_liner_regression(v, vx, v[0:len(v):2], names[0], file_location)
    result['v_vy'] = li_liner_regression(v, vy, v[0:len(v):2], names[1], file_location)
    result['scale_vx'] = li_liner_regression(scale, vx, scale[0:len(scale):2], names[2], file_location)
    result['scale_vy'] = li_liner_regression(scale, vy, scale[0:len(scale):2], names[3], file_location)
    result['density_vx'] = li_liner_regression(density, vx, density[0:len(density):2], names[4], file_location)
    result['density_vy'] = li_liner_regression(density, vy, density[0:len(density):2], names[5], file_location)
    result['viscosity_vx'] = li_liner_regression(viscosity, vx, viscosity[0:len(viscosity):2], names[6], file_location)
    result['viscosity_vy'] = li_liner_regression(viscosity, vy, viscosity[0:len(viscosity):2], names[7], file_location)

    return result


def li_multiple_plot(length, file_location=''):
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.figsize'] = (8.0, 5.0)

    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    for i in range(length):
        csv_data = pd.read_csv(file_location + "sand_" + str(i) + ".csv", header=None, names=['x', 'y'])
        plt.plot(range(csv_data.shape[0]), csv_data['y'], label='video_' + str(i))
    name = Config.UPLOAD_IMAGE_PATH + 'multiple_lines.png'
    plt.legend()
    plt.savefig(name)
    plt.close()

    return name


def get_multiple_iback(length):
    image_locatoion = Config.UPLOAD_IMAGE_PATH
    document_location = Config.SAVE_DOCUMENT_PATH
    results = []
    for id in range(length):
        with open(document_location + "site_" + str(id) + ".txt", "r+") as  f:
            a = f.readlines()
            frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
        image_info = cv.imread(image_locatoion + 'iblack_' + str(id) + '.png')
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
    sand_area_contraction('#曲线各部分面积对比', '面积（m^2）', '',
                          [0, 0, 251, 9780])
