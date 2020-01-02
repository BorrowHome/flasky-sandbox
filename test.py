import csv

import cv2

from app.utils.drawRedrect import pic_to_red
from app.utils.sand_area import Point
from app.utils.zuobiao import PictureSub

sand_coordinate = csv.reader(open('sand.csv', 'r'))
# 单路正向
# 回路0
sum = 0
points = []
for volume in sand_coordinate:
    points.append(Point(volume[0], volume[1]))
    sum = sum + 1

print(points[0].x)

for tmp in range(sum, 0, -1):
    pass

red_png = pic_to_red("currentframe.png")
picture_sub = PictureSub()
src1 = cv2.imread(red_png)
locate = picture_sub.left_up(src1)
locate_remote = picture_sub.right_down(src1)
move_x = locate_remote['list_x'] - locate['list_x']
move_y = locate_remote['list_y'] - locate['list_y']
print(locate['list_x'], locate['list_y'], move_x, move_y)
with open("site.txt", 'w') as f:
    f.write(str(locate['list_x']) + '\n')
    f.write(str(locate['list_y']) + '\n')
    f.write(str(move_x) + '\n')
    f.write(str(move_y) + '\n')
