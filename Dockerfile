FROM ubuntu:16.04

MAINTAINER AUTHOR liliangbin
ENV DEBIAN_FRONTEND noninteractive

USER root

# Modify apt-get to aliyun mirror
RUN sed -i 's/archive.ubuntu/mirrors.aliyun/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install wget

RUN wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
RUN tar -xvJf Python-3.7.0.tar.xz
# Install necessary library
RUN apt-get -y install  python3 python3-dev python3-pip

RUN apt-get install -f -y

# Modify timezone to GTM+8
ENV TZ=Asia/Shanghai
RUN apt-get -y install tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Modify locale
RUN apt-get -y install locales
RUN locale-gen en_US.UTF-8
RUN echo "LANG=\"en_US.UTF-8\"" > /etc/default/locale && \
    echo "LANGUAGE=\"en_US:en\"" >> /etc/default/locale && \
    echo "LC_ALL=\"en_US.UTF-8\"" >> /etc/default/locale


# Modify pip mirror
RUN mkdir -p /root/.pip
RUN echo "[global]" > /root/.pip/pip.conf && \
    echo "index-url=http://mirrors.aliyun.com/pypi/simple/" >> /root/.pip/pip.conf && \
    echo "[install]" >> /root/.pip/pip.conf && \
    echo "trusted-host=mirrors.aliyun.com" >> /root/.pip/pip.conf

RUN pip install --upgrade pip
RUN python --version
WORKDIR /flask-sandbox

#RUN  adduser -D flasky
#USER flasky
# 添加用户后可能会导致文件目录的访问没有权限
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY . .

# CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]

EXPOSE 5000
ENTRYPOINT ["./run.sh"]