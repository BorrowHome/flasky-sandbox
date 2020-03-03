import json

from docx.shared import Mm
from docxtpl import InlineImage
from flask import request, render_template

from app.utils.docx import set_sand_docxtpl
from . import main




@main.route('/test_report/', methods=['GET', 'POST'])
def test_report():
    if request.method == 'POST':

        origin_data = request.get_data()
        str_data = str(origin_data, encoding='utf-8')
        dict_data = json.loads(str_data)

        with open('data.json', 'w') as f:
            json.dump(dict_data, f)

        set_sand_docxtpl(dict_data)
        return "数据"
    else:
        return render_template('test_report.html')


@main.route('/update_report/', methods=['GET'])
def update_report():

    with open('data.json', 'r') as f:
        dict_data = json.load(f)

    set_sand_docxtpl(dict_data)
    return "update data"
