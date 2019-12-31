from PIL import Image

#########################################根据视频中的红线重新画红线
i = 1
j = 1
img = Image.open("currentframe.png")  # 读取系统的内照片
print(img.size)  # 打印图片大小

width = img.size[0]  # 长度
height = img.size[1]  # 宽度
for i in range(0, width):  # 遍历所有长度的点
    for j in range(0, height):  # 遍历所有宽度的点
        data = (img.getpixel((i, j)))  # 打印该图片的所有点

        # print (i,j,data)#打印每个像素点的颜色RGBA的值(r,g,b,alpha)
        # print (data[0])#打印RGBA的r值
        if (data[0] >= 90 and data[1] >= 30 and data[1] <= 70 and data[2] >= 40 and data[
            2] <= 70):  # RGBA的r值大于170，并且g值大于170,并且b值大于170
            img.putpixel((i, j), (255, 0, 0, 255))  # 则这些像素点的颜色改成大红色

img = img.convert("RGB")  # 把图片强制转成RGB

img.save("firstFrame3.jpg")  # 保存修改像素点后的图片
