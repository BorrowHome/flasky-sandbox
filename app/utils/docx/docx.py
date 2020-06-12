import os

import jinja2
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

from app.utils.docx.report_utils import li_multiple_plot, get_result, get_multiple_iback, sand_area_contraction
from config import Config


def set_sand_docxtpl(dict_data, location=''):
    ites = dict_data['tests']['samples']
    path_in = './app/static/video/'
    path_out = '../static/video/'
    print(dict_data)
    print(dict_data['experiment'])
    print('\n')
    print(dict_data['tests'])
    print('dict_dat')
    if location == '' or location == 'index' or location is None or location == ' ':
        video_names = []

        for dirpath, dirnames, filenames in os.walk(path_in):
            for filename in filenames:
                # dir_file_name = os.path.join(dirpath, filename)
                dir_file_name = filename
                if os.path.splitext(dir_file_name)[1] == '.mp4':  # (('./app/static/movie', '.mp4'))
                    print(dir_file_name)
                    video_names.append(path_out + dir_file_name)

        length = len(video_names)
    else:
        ips = []
        document_path = Config.SAVE_DOCUMENT_PATH

        with open(document_path + "ipcConfig.txt", "r+") as  f:
            a = f.readlines()
        for i in a:
            ips.append(i)
        length = len(ips)

    print("一共有多少个数据")
    doc = DocxTemplate("tpl.docx")

    imge_file_location = Config.UPLOAD_IMAGE_PATH
    document_file_location = Config.SAVE_DOCUMENT_PATH
    multiplt_lines = li_multiple_plot(length, document_file_location)
    results_frame = get_result(ites, imge_file_location)
    name_list = ['v_vx', 'v_vy', 'scale_vx', 'scale_vy', 'density_vx', 'density_vy', 'viscosity_vx', 'viscosity_vy']
    results_done = run_name(name_list, doc, results_frame)
    li_result = get_multiple_iback(length)
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
    context = {
        'device': dict_data['device'],
        'experiment': dict_data['experiment'],
        'tests': dict_data['tests'],
        'line_relations': results_frame,
        'multiple_lines': InlineImage(doc, multiplt_lines, Mm(100)),
        'contrast': li_result,
        'li_test': [0, 1, 2, 3, 6]
    }
    jinja_env = jinja2.Environment(autoescape=True)

    doc.render(context)
    file_location = dict_data['experiment']['file_location']
    print("file location===>" + file_location)
    if (os.path.exists(file_location)):
        print("rush")
        doc.save(file_location + "/generated_doc.docx")
    else:
        print("cant")
        doc.save("generated_doc.docx")
    doc.save(document_file_location + "generated_doc.docx")


def run_name(name_list, tpl, results_frame):
    for name in name_list:
        results_frame[name]['a'] = round(results_frame[name]['a'][0][0], 2)
        results_frame[name]['b'] = round(results_frame[name]['b'][0], 2)
        results_frame[name]['file_name'] = InlineImage(tpl, results_frame[name]['file_name'],
                                                       Mm(100))
    return results_frame
