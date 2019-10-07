# -*- coding: utf-8 -*-


from flask import request, render_template, redirect, url_for,flash

from config import Config
from . import main
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@main.route('/upload/', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        videos = request.files.getlist('video')
        # TODO // 对图像的后缀以及名字的合法性进行鉴定
        for video in videos:
            print(video.filename)
            print(video.filename)
            print(video.filename, os.path.abspath(video.filename))
            if allowed_file(video.filename):
                file_path = Config.UPLOAD_PATH+ os.sep + os.path.split(os.path.abspath(video.filename))[1]
                video.save(file_path)
            else:
                flash('Wrong file type!', 'danger')
                return redirect(url_for('.index'))
        flash("Upload successfully!",'success')#@hehao
            # video.save(Config.UPLOAD_PATH + video.filename)

        return redirect(url_for('.index'))
