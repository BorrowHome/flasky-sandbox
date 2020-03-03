import jinja2
from docx.shared import Mm
from docxtpl import DocxTemplate
from docxtpl import InlineImage

from app.utils.report_utils import li_multiple_plot, get_result, get_multiple_iback, sand_area_contraction
from config import Config

doc = DocxTemplate("tpl.docx")
myimage = InlineImage(doc, 'info.jpg', width=Mm(20))


def run_name(name_list, tpl, results_frame):
    for name in name_list:
        results_frame[name]['a'] = round(results_frame[name]['a'][0][0], 2)
        results_frame[name]['b'] = round(results_frame[name]['b'][0], 2)
        results_frame[name]['file_name'] = InlineImage(tpl, results_frame[name]['file_name'],
                                                       Mm(100))
    return results_frame


device = {
    'name': '设备名字',
    'produce_company': '设备生产厂家',
    'produce_time': '生产时间',
    'maintain_time': '保养时间',
    'responsible_man': '责任人',
    'experimenters': '实验人员',
    'own_company': '单位名称'
}

experiment = {
    'fluid': {
        'name': '压裂液名称',
        'viscosity': '压裂液粘度',
        'density': '压裂液密度',

    },
    'proppant': {
        'name': '支撑剂类型',
        'density': '支撑剂密度',
        'aperture': '支撑剂孔径'
    },
    'file_location': '实验文档的存放位置'
}

items = [
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 2.000, 'vy': 1.000, 'v': 1.2, 'scale': 23, 'density': 1800, 'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 2.000, 'vy': 1.000, 'v': 1.2, 'scale': 23, 'density': 1800, 'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 2.000, 'vy': 1.000, 'v': 1.2, 'scale': 23, 'density': 1800, 'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 2.000, 'vy': 1.000, 'v': 1.2, 'scale': 23, 'density': 1800, 'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 2.000, 'vy': 1.000, 'v': 1.2, 'scale': 23, 'density': 1800, 'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 2.000, 'vy': 1.000, 'v': 1.2, 'scale': 23, 'density': 1800, 'viscosity': 30}
]

tests = {
    'samples': items,
    'average_vx': 2,
    'average_vy': 4
}

ites = [
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 4.000, 'vy': 4.000, 'v': 5, 'scale': 23, 'density': 1800,
     'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 2.000, 'vy': 3.000, 'v': 4, 'scale': 23, 'density': 1800,
     'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 1.000, 'vy': 2.000, 'v': 3, 'scale': 23, 'density': 1800,
     'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': 0.000, 'vy': 1.000, 'v': 2, 'scale': 23, 'density': 1800,
     'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': -1.000, 'vy': 0.000, 'v': 1.2, 'scale': 23, 'density': 1800,
     'viscosity': 30},
    {'lx': 10, 'ly': 5, 'time': 5, 'vx': -2.000, 'vy': -2.000, 'v': 0, 'scale': 23, 'density': 1800,
     'viscosity': 30}

]
imge_file_location = Config.UPLOAD_IMAGE_PATH
document_file_location = Config.SAVE_DOCUMENT_PATH
# multiple_lines
multiplt_lines = li_multiple_plot(3, document_file_location)
# results_frame
results_frame = get_result(ites, imge_file_location)

name_list = ['v_vx', 'v_vy', 'scale_vx', 'scale_vy', 'density_vx', 'density_vy', 'viscosity_vx', 'viscosity_vy']
results_done = run_name(name_list, doc, results_frame)
# 可以用一个函数搞定 传递的是引用
print()

imge_file_location = Config.UPLOAD_IMAGE_PATH
document_file_location = Config.SAVE_DOCUMENT_PATH

li_result = get_multiple_iback(3)
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

print(li_result)

context = {
    'device': device,
    'experiment': experiment,
    'tests': tests,
    'line_relations': results_frame,
    'multiple_lines': InlineImage(doc, multiplt_lines, Mm(100)),
    'contrast': li_result,
    'li_test': [0, 1, 2, 3, 6]
}



# s 是jinjia2的关键字。不能被我们作为变量使用


jinja_env = jinja2.Environment(autoescape=True)

doc.render(context)
doc.save("generated_doc.docx")
