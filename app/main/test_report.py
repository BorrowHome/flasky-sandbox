import json

from flask import request, render_template

from app.utils.report_utils import li_liner_regression
from . import main


@main.route('/test_report/', methods=['GET', 'POST'])
def test_report():
    if request.method == 'POST':

        origin_data = request.get_data()
        str_data = str(origin_data, encoding='utf-8')
        dict_data = json.loads(str_data)
        ites = dict_data['tests']


        names = ['流速与水平速度关系回归式', '流速与垂直速度关系回归式',
                 '砂比与水平速度关系回归式', '砂比与垂直速度关系回归式',
                 '支撑剂密度与水平速度关系回归式', '支撑剂密度与垂直速度关系回归式',
                 '压裂液粘度与水平速度关系回归式', '压裂液粘度与垂直速度关系回归式']


        return "数据"
    else:
        return render_template('test_report.html')
