# INFO 2019/12/28 17:01 liliangbin  框的坐标点

class Site(object):

    def __init__(self, locate_x, locate_y, move_x, move_y):
        self.locate_x = locate_x
        self.locate_y = locate_y
        self.move_x = move_x
        self.move_y = move_y
        self.locate_result_x = locate_x + move_x
        self.locate_result_y = locate_y + move_y

    @staticmethod
    def read_site(location):
        try:
            with open(location, "r+") as  f:
                a = f.readlines()
                print(a)
                frame_location = Site(int(a[0]), int(a[1]), int(a[2]), int(a[3]))
        except IOError:
            print('not  found file or read error')
            frame_location = Site(1, 1, 1, 1)

        return frame_location

    def get_site(self):

        site_left_top = [str(self.locate_x), str(self.locate_y)]
        site_left_bottom = [str(self.locate_x), str(self.locate_result_y)]
        site_right_top = [str(self.locate_result_x), str(self.locate_y)]
        site_right_bottom = [str(self.locate_result_x), str(self.locate_result_y)]
        return {
            'site_left_top': site_left_top,
            'site_left_bottom': site_left_bottom,
            'site_right_top': site_right_top,
            'site_right_bottom': site_right_bottom,
        }


if __name__ == '__main__':
    a = Site(5, 6, 7, 8)
    print(a.move_y)
