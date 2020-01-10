FROM python:3.7-alpine3.9
WORKDIR /Project/flasky

RUN apk add --no-cache --update \
    python3 python3-dev g++ \
    gfortran musl-dev \
    libffi-dev openssl-dev

# 安装numpy需要提前有一些环境
ENV FLASK_APP flask.py
ENV FLASK_CONFIG docker

#RUN  adduser -D flasky
#USER flasky
# 添加用户后可能会导致文件目录的访问没有权限
COPY requirements.txt ./
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r requirements.txt

COPY . .

# CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]

EXPOSE 5000
ENTRYPOINT ["./run.sh"]