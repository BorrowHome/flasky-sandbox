import os

from flask_script import Manager
from gevent import monkey
from gevent import pywsgi

from app import create_app

# monkey.patch_all()
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

server = pywsgi.WSGIServer(("127.0.0.1", 8082), app)
server.serve_forever()

