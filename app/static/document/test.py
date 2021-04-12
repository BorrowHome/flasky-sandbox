# import csv
# # with open("sand_VideoMosaic.csv", "w+") as f:
# #     f.write('1')
# #     print(qwe)
# #     print('\n'.join(qwe))
# with open("sand_VideoMosaic.csv", "a+") as f:
#     for i in range(3000):
#         f.write('{},0\n'.format(i))
# # with open("sand_video.csv", "a+") as f:
# #     writer = csv.writer(f)
# #     for i in range(1000):
# #         if


# listx = []
# listy = []
# # 根据拼接视频csv 上传res数据
# with open("sand_VideoMosaic.csv", "r+") as  f:
#     wadad = f.read().strip().split('\n')
#     for i in wadad:
#         listx.append(int(i.split(',')[0]))
#         listy.append(int(i.split(',')[1]))
# print(listx)
# print(listy)

# video_names=[1,2,3]
# video_name=2
# videoOrder=video_names.index(video_name)
# print(videoOrder)
import csv
CoordinateAddNumb=1741
res={
}
res['list_x'] = []
res['list_y'] = []
for i in range(607):
    res['list_x'].append(i)
    res['list_y'].append(i)

with open("sand_VideoMosaic.csv", "r+") as  f:
    qwe = f.read().strip().split('\n')
    # print(len(res['list_x']), len(res['list_y']))
    for i in range(607):
        qwe[CoordinateAddNumb + i] = qwe[CoordinateAddNumb + i].split(',')[0] + ',{}'.format([i])