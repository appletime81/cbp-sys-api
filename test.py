from docxtpl import DocxTemplate

doc = DocxTemplate("bill_draft_tpl.docx")
context = {'address': "Level 30, Tower 1, Kowloon Commerce Centre, No.51 Kwai Cheong Road, Kwai Chung, New Territories, Hong Kong"}
doc.render(context)
doc.save("generated_doc.docx")
