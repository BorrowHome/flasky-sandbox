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

