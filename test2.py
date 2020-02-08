from docxtpl import DocxTemplate

doc = DocxTemplate("test.docx")
context = {'col': "World company"}
doc.render(context)
doc.save("generated_doc.docx")
