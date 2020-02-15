import cv2
from flask import request, render_template, redirect, url_for, flash

from app.utils.frame import base64_to_png
from config import Config
from . import main

@main.route('/test_report', methods=['GET', 'POST'])
def test_report():
    if request.method=='POST':
        return "none"
    else:
        return render_template('test_report.html')