import base64

import cv2
import numpy as np


def base64_to_png(str):
    str = str.split(',')[1]

    #  在逗号以后的7才是编码数据 前面是协议和格式
    if (len(str) % 3 == 1):
        str += "=="
    elif (len(str) % 3 == 2):
        str += "="

    image = base64.b64decode(str)
    np_array = np.fromstring(image, np.uint8)
    # 生成cv2 需要的数据类型
    img_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    print(img_np.shape)

    return img_np
