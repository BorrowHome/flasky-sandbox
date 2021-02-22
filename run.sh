#!/bin/bash
export FLASK_APP=flasky.py
export FLASK_DEBUG=1
echo 'run a flask app '

python -m flask run -h 0.0.0.0 -p 8083

# python -m 用于直接引入这个模块跑文件
