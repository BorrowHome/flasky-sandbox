import math


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Helen_formula(object):

    def get_area_of_poly_gon(self, points):
        # 计算多边形面积
        area = 0
        if (len(points) < 3):
            raise Exception("error")

        p1 = points[0]
        for i in range(1, len(points) - 1):
            p2 = points[i]
            p3 = points[i + 1]

            # 计算向量
            vecp1p2 = Point(p2.x - p1.x, p2.y - p1.y)
            vecp2p3 = Point(p3.x - p2.x, p3.y - p2.y)

            # 判断顺时针还是逆时针，顺时针面积为正，逆时针面积为负
            vecMult = vecp1p2.x * vecp2p3.y - vecp1p2.y * vecp2p3.x  # 判断正负方向比较有意思
            sign = 0
            if (vecMult > 0):
                sign = 1
            elif (vecMult < 0):
                sign = -1

            triArea = self.get_area_of_triangle(p1, p2, p3) * sign
            area += triArea
        return abs(area)

    def get_area_of_triangle(self, p1, p2, p3):
        '''计算三角形面积   海伦公式'''
        area = 0
        p1p2 = self.get_line_length(p1, p2)
        p2p3 = self.get_line_length(p2, p3)
        p3p1 = self.get_line_length(p3, p1)
        s = (p1p2 + p2p3 + p3p1) / 2
        area = s * (s - p1p2) * (s - p2p3) * (s - p3p1)  # 海伦公式
        area = math.sqrt(area)
        return area

    def get_line_length(self, p1, p2):
        '''计算边长'''
        length = math.pow((p1.x - p2.x), 2) + math.pow((p1.y - p2.y), 2)  # pow  次方
        length = math.sqrt(length)
        return length


def main():
    points = []
    x = [7, 11, 31, 55, 75, 77, 80, 94, 122, 172, 183, 201, 248, 274, 296, 328, 371, 405, 424, 447, 467, 480, 453, 400,
         328, 259, 78, 8]
    y = [254, 257, 258, 253, 252, 253, 254, 256, 256, 247, 246, 246, 254, 256, 256, 256, 256, 256, 255, 251, 245, 242,
         241, 240, 239, 238, 236, 230]
    for index in range(len(x)):
        points.append(Point(x[index], y[index]))

    helen = Helen_formula()
    area = helen.get_area_of_poly_gon(points)
    print(area)
    print(math.ceil(area))
    # assert math.ceil(area)==1


if __name__ == '__main__':
    main()
    print("OK")
