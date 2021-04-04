import multiprocessing
import os
import sys

from flask_cors import CORS
from flask_script import Manager

from app import create_app

# basedir = os.path.abspath(os.path.dirname(__file__))
basedir, filename = os.path.split(os.path.abspath(sys.argv[0]))
# exe 运行的路径
app = create_app(basedir)
CORS(app, supports_credentials=True)
manager = Manager(app)
count = multiprocessing.cpu_count()
print('main to  ', basedir)
# app.__setattr__('static_folder', basedir + '\\app\\static')

if __name__ == "__main__":
    from waitress import serve

    # waitress官方有更多详细的启动方式
    serve(app, listen='0.0.0.0:8082', threads=count * 2 + 1)
