import multiprocessing
import os

from flask_cors import CORS
from flask_script import Manager

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
CORS(app, supports_credentials=True)
manager = Manager(app)
count = multiprocessing.cpu_count()
print(count)
if __name__ == "__main__":
    from waitress import serve

    # waitress官方有更多详细的启动方式
    serve(app, listen='0.0.0.0:8082', threads=count * 2 + 1)
