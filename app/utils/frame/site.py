# INFO 2019/12/28 17:01 liliangbin  框的坐标点

class Site(object):

    def __init__(self, locate_x, locate_y, move_x, move_y):
        self.locate_x = locate_x
        self.locate_y = locate_y
        self.move_x = move_x
        self.move_y = move_y


if __name__ == '__main__':
    a = Site(5, 6, 7, 8)
    print(a.move_y)
