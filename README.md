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
- mkl-fft  安装不上
- pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

### todolist 
- 把以前的算法修改，需要有四个点的坐标。
- echart 图片的保存
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

- 