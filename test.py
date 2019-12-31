import csv

from app.utils.sand_area import Point

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