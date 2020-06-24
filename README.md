# flasky-sandbox

- 砂箱砂子轮廓检测客户端

### 环境建立(推荐使用anaconda)

- sh init.sh  
- cmd 运行策略问题，使用其他的shell  我使用的是cmder来跑 

### 运行

#### 测试环境

- sh run.sh  启动测试环境
- 默认具体配置可自己手动修改，默认使用debug 模式。
- git clone --depth 3   url  # 下载文件过大的时候解决
- pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package 
- 临时安装使用

#### 实际环境（挑选一个）
 
- python waitress_manage.py  使用waitress 来运行实际环境
- python gevent_manage.py 使用gevent来作为实际环境，但是ipc有问题。

### docker （Dockerfile 应该是可以用的)

- docker build -t liliangbin/sandbox:v1 .
- docker run -it --rm liliangbin/sandbox:v1 bash
- pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

### todolist 

- echart.js  重构为使用服务端运行pyecharts
- 添加边框识别算法的方式
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
 - csv 文件需要平滑处理，可能有噪声点
 - python nmap  很牛逼
 - 设置背景
 
###  
