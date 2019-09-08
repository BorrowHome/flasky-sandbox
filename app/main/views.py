# -*- coding: utf-8 -*-

from . import main
from .. import db
from ..models import User
from flask import render_template, request
import time
from ..models import PoseToLocation


@main.route('/')
def index():
    return render_template('index.html', name='index')


@main.route('/query')
def query():
    user = User()
    user.username = 'user_name_test' + str(time.time())
    db.session.add(user)
    db.session.commit()
    print 'commit '
    return render_template('web_wideo.html')
