# import pandas as pd
#
# data = pd.read_excel('result.xlsx', header=0,
#                      names=['pp', 'pf', 'dp', 'ua', 'c', 'w', 'q', 'h', 'fai', 'vcs', 'vpx', 'ueq', 'heq'])
#
# x = list(data.get('pp').astype(float))
#
# print(x)

import cv2
import numpy as np
qwe=cv2.imdecode(np.fromfile(r'D:\dachuang\NewProject1\app\static\image\back_视频3.png',dtype=np.uint8),cv2.IMREAD_COLOR)
print(qwe)
background = cv2.imread(r'D:\dachuang\NewProject1\app\static\image\back_视频3.png')
print(background)