import jinja2
from docx.shared import Mm
from docxtpl import DocxTemplate
from docxtpl import InlineImage

from app.utils.report_utils import li_multiple_plot,get_result,li_liner_regression,sand_area_contraction
from config import Config

doc = DocxTemplate("tpl.docx")
myimage = InlineImage(doc, 'info.jpg', width=Mm(20))

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
imge_file_location = Config.UPLOAD_IMAGE_PATH
document_file_location = Config.SAVE_DOCUMENT_PATH

multiplt_lines = li_multiple_plot(3, document_file_location)

results=get_result(items,imge_file_location )

context = {
    'device': device,
    'experiment': experiment,
    'tests': tests

}

# 记录一个坑，items 是jinjia2的关键字。不能被我们作为变量使用


jinja_env = jinja2.Environment(autoescape=True)

doc.render(context)
doc.save("generated_doc.docx")
