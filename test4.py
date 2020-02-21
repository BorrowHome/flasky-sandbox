import pandas as pd

from app.utils.report_utils import li_liner_regression, li_multiple_plot, get_result, get_multiple_iback, \
    sand_area_contraction
from config import Config

# plt.show()


if __name__ == '__main__':
    sand = pd.read_csv("sand_2.csv", header=None, names=['x', 'y'])
    x = sand['x']

    y = sand['y']
    test_li = sand['x']

    test_li = test_li[0:len(test_li):6].values
    result = li_liner_regression(x, y, test_li, "第二项回归曲线")
    print(result['a'][0][0])

    ites = [
        {'lx': 10, 'ly': 5, 'time': 5, 'vx': 4.000, 'vy': 4.000, 'v': 5, 'scale': 23, 'density': 1800,
         'viscosity': 30},
        {'lx': 10, 'ly': 5, 'time': 5, 'vx': 2.000, 'vy': 3.000, 'v': 4, 'scale': 23, 'density': 1800,
         'viscosity': 30},
        {'lx': 10, 'ly': 5, 'time': 5, 'vx': 1.000, 'vy': 2.000, 'v': 3, 'scale': 23, 'density': 1800,
         'viscosity': 30},
        {'lx': 10, 'ly': 5, 'time': 5, 'vx': 0.000, 'vy': 1.000, 'v': 2, 'scale': 23, 'density': 1800,
         'viscosity': 30},
        {'lx': 10, 'ly': 5, 'time': 5, 'vx': -1.000, 'vy': 0.000, 'v': 1.2, 'scale': 23, 'density': 1800,
         'viscosity': 30},
        {'lx': 10, 'ly': 5, 'time': 5, 'vx': -2.000, 'vy': -2.000, 'v': 0, 'scale': 23, 'density': 1800,
         'viscosity': 30}

    ]

    imge_file_location = Config.UPLOAD_IMAGE_PATH
    document_file_location = Config.SAVE_DOCUMENT_PATH
    result = get_result(ites, imge_file_location)

    for i in range(4):
        print(i)
    print(result)
    li = li_multiple_plot(3, document_file_location)
    print(li)
    li_result = ''

    li_result = get_multiple_iback(3)

    print(li_result)

    test = [
        {
            'area':
                {
                    'areas': [48800, 73573, 69631, 49901],
                    'added': ['50.76%', '-5.36%', '-28.34%'],
                    'averageAreas': 60476.25
                },
            'height':
                {
                    'height': [191.7, 255.31, 274.12, 186.31], 'added': ['33.18%', '7.37%', '-32.03%'],
                    'averageHeight': 226.86
                }
        },
        {
            'area':
                {
                    'areas': [0, 0, 251, 9780],
                    'added': ['0.00%', '0.00%', '3796.41%'],
                    'averageAreas': 2507.75
                },
            'height':
                {
                    'height': [0, 0, 393.8, 151.27],
                    'added': ['0.00%', '0.00%', '-61.59%'],
                    'averageHeight': 136.27
                }
        },
        {
            'area':
                {
                    'areas': [2588, 2360, 2470, 844], 'added': ['-8.81%', '4.66%', '-65.83%'],
                    'averageAreas': 2065.5},
            'height':
                {'height': [20.98, 20.28, 23.14, 19.08], 'added': ['-3.34%', '14.10%', '-17.55%'],
                 'averageHeight': 20.87}}
    ]
    i = 0
    for item in li_result:
        print(item['area']['areas'])
        item['area_plt'] = sand_area_contraction('曲线各部分面积对比#' + str(i), '面积（m^2）', imge_file_location,
                                                 item['area']['areas'])
        item['height_plt'] = sand_area_contraction('各部分高度对比#' + str(i), '高度（m）', imge_file_location,
                                                   item['height']['heights'])
        i += 1

    print(li_result)
