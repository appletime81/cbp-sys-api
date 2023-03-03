from docxtpl import DocxTemplate

doc = DocxTemplate("test_template.docx")
context = {"name": "World company"}
doc.render(context)
doc.save("generated_doc.docx")
