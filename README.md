# flasky-sandbox
- 沙箱沙子轮廓检测客户端

### 环境建立(推荐使用anaconda)
- sh init.sh  


- 下面是直接复现anaconda 环境 但不会安装使用pip 安装的东西 可忽略  
- conda env export > environment.yaml
- conda env create -f environment.yaml

- 只用安装flask-SQLAlchemy  它里面有使用mysql 的链接器，不用额外安装
#### 运行
- sh run.sh
- 默认具体配置可自己手动修改，默认使用debug 模式。
- git clone --depth 3   url  # 下载文件过大的时候解决
- pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package 
- 临时安装使用

-  docker build -t liliangbin/sandbox:v1 .
- docker run -it --rm liliangbin/sandbox:v1 bash
- mkl-fft  安装不上
- pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
- 发生冲突时  git pull origin master  放弃本地修改，更改到最新的分支
### todolist 
- echart.js  重构为使用服务端运行pyecharts
- 添加边框识别算法的方式
- PIL使用的是python2 
- apk is the package manager for Alpine. You're using Ubuntu. You need to use apt-ge

- ```shell
    FROM python:3.7.2-alpine3.9
    RUN apk add --no-cache python3-dev libstdc++ && \
        apk add --no-cache g++ && \
        ln -s /usr/include/locale.h /usr/include/xlocale.h && \
        pip3 install numpy && \
        pip3 install pandas
  ```
 - 视频一起处理的时候，每个视频都需要用每个视频的第一帧么，框选边框的时候边框也需要新的边框么
 - 每个视频的沙子面积和比例都需要显示出来么。
 - 那个文档需要录入哪些信息，有没有什么标注的
 - csv 文件需要平滑处理，可能有噪声点
 - python nmap  很牛逼
 - 设置背景
 
 
https://github.com/cisco/openh264/releases  
h264  需要的依赖库
exists  多在于子查询中。 
