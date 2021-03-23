import json
import os

import jinja2
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

from app.utils.docx.report_utils import li_multiple_plot, get_result, get_multiple_iback, sand_area_contraction
from config import Config


#  写入docx 中
def set_sand_docxtpl(dict_data, location=''):
    path_in = './app/static/video/'
    path_out = '../static/video/'
    print(dict_data)
    print(dict_data['experiment'])
    print('\n')
    names = []
    if location == '' or location == 'index' or location is None or location == ' ':
        video_names = []

        for dirpath, dirnames, filenames in os.walk(path_in):
            for filename in filenames:
                # dir_file_name = os.path.join(dirpath, filename)
                dir_file_name = filename
                if os.path.splitext(dir_file_name)[1] == '.mp4':  # (('./app/static/movie', '.mp4'))
                    print(dir_file_name)
                    names.append(dir_file_name.split('.')[0])
                    video_names.append(path_out + dir_file_name)

        length = len(video_names)

    else:
        ips = []
        document_path = Config.SAVE_DOCUMENT_PATH

        with open(document_path + "ipcConfig.txt", "r+") as  f:
            a = f.readlines()
        for i in a:
            ips.append(i)
            names.append(''.join(i.split('.')))
        length = len(ips)

    print("一共有多少个数据")
    doc = DocxTemplate("tpl.docx")

    imge_file_location = Config.UPLOAD_IMAGE_PATH
    document_file_location = Config.SAVE_DOCUMENT_PATH
    #  多折线图
    multiplt_lines = li_multiple_plot(length, file_location=document_file_location, names=names)
    # 多个图像的线性回归关系
    print('获取多级线性关系')

    results_frame = get_result(imge_file_location)
    # 放入docx模板中
    # name_list = ['v_vx', 'v_vy', 'scale_vx', 'scale_vy', 'density_vx', 'density_vy', 'viscosity_vx', 'viscosity_vy']
    print('线性关系入docx')

    run_name(doc, results_frame)
    # 获取面积比例
    print('获取面积比例开始')
    print(names)
    li_result = get_multiple_iback(length, names=names)
    i = 0
    for item in li_result:
        print(item['area']['areas'])
        item['area_plt'] = sand_area_contraction('曲线各部分面积对比#' + str(i), '面积（m^2）', imge_file_location,
                                                 item['area']['areas'])
        item['height_plt'] = sand_area_contraction('各部分高度对比#' + str(i), '高度（m）', imge_file_location,
                                                   item['height']['heights'])
        i += 1
        item['area_plt'] = InlineImage(doc, item['area_plt'], Mm(70))
        item['height_plt'] = InlineImage(doc, item['height_plt'], Mm(70))
    print('处理面积比例完毕')
    #  将数据放入文档中
    context = {
        'device': dict_data['device'],
        'experiment': dict_data['experiment'],
        # 'tests': dict_data['tests'],
        'line_relations': results_frame,
        'multiple_lines': InlineImage(doc, multiplt_lines, Mm(100)),
        'contrast': li_result,
        'li_test': [0, 1, 2, 3, 6]
    }
    jinja_env = jinja2.Environment(autoescape=True)
    print('开始准备存入docx ')

    doc.render(context)
    print('存入docx ')
    file_location = dict_data['experiment']['file_location']
    print("file location===>" + file_location)
    if (os.path.exists(file_location)):
        print("save docx to {}".format(file_location))
        doc.save(file_location + "/generated_doc.docx")
    else:
        print("cant find the location save to default location")
        doc.save("generated_doc.docx")
    doc.save(document_file_location + "generated_doc.docx")


# 对文件处理
def run_name(tpl, results_frame):
    for key in results_frame:
        name = results_frame.get(key)
        print('item {}'.format(name))
        name['a'] = round(name['a'][0][0], 2)
        name['b'] = round(name['b'][0], 2)
        name['file_name'] = InlineImage(tpl, name['file_name'],
                                        Mm(100))


def get_formatua_data():
    document_location = Config.SAVE_DOCUMENT_PATH

    with open(document_location + 'excel_save.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
    print(data)
    return data
