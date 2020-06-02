import os

from flask_script import Manager
from gevent import monkey

from app import create_app

monkey.patch_all()
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def runserver_gevent():
    from gevent import pywsgi
    server = pywsgi.WSGIServer(("0.0.0.0", 8080), app)
    server.serve_forever()


if __name__ == "__main__":
    manager.run()
