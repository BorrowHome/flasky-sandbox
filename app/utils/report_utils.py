import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model

from config import Config


# plt.show()


def sand_area_contraction(title, y_axies, file_location, num_list=[20, 20, 40, 50], color='b'):
    name_list = ['第一区', '第二区', '第三区', '第四区']
    num_list = num_list

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.figsize'] = (8.0, 5.0)

    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.bar(range(len(num_list)), num_list, tick_label=name_list, color=color)
    plt.title('测试')
    plt.ylabel(y_axies)
    # plt.xlabel('X axis')
    plt.grid(axis='y')
    plt.savefig(file_location + title + '.png')
    return file_location + title + '.png'


def li_liner_regression(x, y, test_x, name, file_location=''):
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
    file_name = name + '.png'
    plt.title(name)
    plt.savefig(file_location + file_name)
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
    return name
