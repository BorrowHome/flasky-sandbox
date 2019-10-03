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

