import cv2

cap = cv2.VideoCapture('rtsp://192.168.1.10:554/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp?real_stream'
                       )
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
# 获取cap视频流的每帧大小
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(size)

fourcc = cv2.VideoWriter_fourcc(*'avc1')
#  格式挺多的，我们可以替换下面的fourcc 为-1  输出支持的格式，然后我们可以查看视频的编码格式
# Failed to load OpenH264 library: openh264-1.8.0-win64.dll
#	Please check environment and/or download library: https://github.com/cisco/openh264/releases
# 相应的依赖库 https://github.com/cisco/openh264/releases
outVideo = cv2.VideoWriter('saveDir.mp4', fourcc, fps, size)
# 获取视频流打开状态
if cap.isOpened():
    rval, frame = cap.read()
    print('true')
else:
    rval = False
    print('False')

tot = 1
c = 1
# 循环使用cv2的read()方法读取视频帧
while rval:
    rval, frame = cap.read()
    cv2.imshow('test', frame)
    # 每间隔20帧保存一张图像帧
    # if tot % 20 ==0 :
    #   cv2.imwrite('cut/'+'cut_'+str(c)+'.jpg',frame)
    #   c+=1
    tot += 1
    print('tot=', tot)
    # 使用VideoWriter类中的write(frame)方法，将图像帧写入视频文件
    outVideo.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('done')  # 在显示窗口中键入q
        break

cap.release()
outVideo.release()
cv2.destroyAllWindows()
