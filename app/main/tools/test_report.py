import json

from flask import request, render_template, jsonify

from app.utils.docx.docx import set_sand_docxtpl
from config import Config
from app.main import main
import pandas as  pd


@main.route('/export_report/', methods=['GET'])
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


@main.route("/excel_save/", methods=['POST'])
def excel_save():
    # print('*' * 51)
    document_location = Config.SAVE_DOCUMENT_PATH
    data = json.loads(request.get_data(as_text=True))
    excel = data.get('list')
    print('运行 excel_save ,保存数据到本地')
    print(excel)
    save_to_excel(excel, document_location + 'result.xlsx')
    with open(document_location + 'excel_save.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(excel))
    return 'df'


@main.route("/recovery_Excel/", methods=['POST'])
def recovery_Excel():
    document_location = Config.SAVE_DOCUMENT_PATH

    with open(document_location + 'excel_save.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
    print('运行 recovery_Excel ,返回本地储存数据')
    print(data)
    return jsonify(data)


@main.route("/report/", methods=['GET', 'POST'])
def report():
    file_location = Config.SAVE_DOCUMENT_PATH
    location = ''  # 报告的存放位置
    if request.method == 'GET':
        with open(file_location + 'data.json', 'r') as f:
            dict_data = json.load(f)

        return jsonify(dict_data)
    else:
        origin_data = request.get_data()
        str_data = str(origin_data, encoding='utf-8')
        dict_data = json.loads(str_data)

        with open(file_location + 'data.json', 'w') as f:
            json.dump(dict_data, f)
        return 'done'


def save_to_excel(data, file_name):
    config = {
        '支撑剂密度': [],
        '压裂液密度': [],
        '支撑剂直径': [],
        '压裂液粘度': [],
        '砂比': [],
        '裂缝宽度': [],
        '排量': [],
        '裂缝高度': [],
        '砂堤孔隙度': [],
        '垂直移动速度': [],
        '水平运移速度': [],
        '平衡流速': [],
        '平衡高度': []
    }
    print('current data======================>')
    print(data)

    if len(data) > 0:
        for key in data:
            config.get('支撑剂密度').append(key.get('pp'))
            config.get('压裂液密度').append(key.get('pf'))
            config.get('支撑剂直径').append(key.get('dp'))
            config.get('压裂液粘度').append(key.get('ua'))
            config.get('砂比').append(key.get('c'))
            config.get('裂缝宽度').append(key.get('w'))
            config.get('排量').append(key.get('q'))
            config.get('裂缝高度').append(key.get('h'))
            config.get('砂堤孔隙度').append(key.get('fai'))
            config.get('垂直移动速度').append(key.get('vcs'))
            config.get('水平运移速度').append(key.get('vpx'))
            config.get('平衡流速').append(key.get('ueq'))
            config.get('平衡高度').append(key.get('heq'))

    df = pd.DataFrame(config)
    df.to_excel(file_name, index=False)
    print('save to excel')


if __name__ == '__main__':
    with open(r'excel_save.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
    save_to_excel(data, 'result.xlsx')
