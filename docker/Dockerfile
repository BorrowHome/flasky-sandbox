FROM ubuntu:16.04

MAINTAINER AUTHOR liliangbin
ENV DEBIAN_FRONTEND noninteractive
ADD sources.list /etc/apt/
ADD Python-3.7.0.tar.xz /root
RUN cd /root && ls
USER root

# Modify apt-get to aliyun mirror
RUN apt-get update && apt-get install -y

RUN apt-get -y install g++ curl vim\
    && apt-get install libssl-dev -y  \
    && apt-get install -y libffi-dev \
    && apt-get install -y make \
    && apt-get install -y libsm6 libxext6 libxrender-dev libglib2.0-dev

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

RUN apt-get -y install wget && pwd && ls

# RUN wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
# RUN tar -xvJf Python-3.7.0.tar.xz
RUN cd /root/Python-3.7.0 \
    && ./configure prefix=/usr/local/python3 \
    && make && make install
RUN rm -rf /usr/bin/python
RUN rm -rf /usr/bin/pip

RUN  ln -s /usr/local/python3/bin/python3.7 /usr/bin/python
RUN  ln -s /usr/local/python3/bin/pip3 /usr/bin/pip
# Install necessary library

RUN python --version
WORKDIR /flask-sandbox

##RUN  adduser -D flasky
##USER flasky
## 添加用户后可能会导致文件目录的访问没有权限
COPY ../requirements.txt ./
#
RUN pip install -r requirements.txt
COPY .. .

