import json

from flask import request, render_template, jsonify

from app.utils.docx.docx import set_sand_docxtpl
from config import Config
from app.main import main


@main.route('/test_report/', methods=['POST'])
def test_report():
    file_location = Config.SAVE_DOCUMENT_PATH
    origin_data = request.get_data()
    str_data = str(origin_data, encoding='utf-8')
    dict_data = json.loads(str_data)

    with open(file_location + 'data.json', 'w') as f:
        json.dump(dict_data, f)

    set_sand_docxtpl(dict_data)
    return jsonify({'success'})


@main.route('/update_report/', methods=['GET'])
def update_report():
    file_location = Config.SAVE_DOCUMENT_PATH
    location = ''  # 报告的存放位置
    with open(file_location + 'data.json', 'r') as f:
        dict_data = json.load(f)
    try:
        set_sand_docxtpl(dict_data, location)
        return "成功"
    except Exception as e:
        print(str(e))
        return str(e)
