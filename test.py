# from docxtpl import DocxTemplate
#
# """
# {{ conteact_person }}
# {{ contact_num }}
# {{ email }}
# {{ recipient }}
# {{ year }}
# {{ month }}
# {{ day }}
# {{ text_number }}
# {{ topic_bank_name }}
# {{ payment_name }}
# {{ chinese_payment }}
# {{ arabic_payment }}
# {{ account_no_1 }}
# {{ account_name }}
# {{ bank }}
# {{ bank_address }}
# {{ account_no_2 }}
# {{ iban }}
# {{ swift }}
# {{ invoice_num }}
# {{ work_title }}
# {{ foreign_currency_demand_deposit_no }}
# """
#
# doc = DocxTemplate("template.docx")
# context = {
#     "file_num": "TPE112013001",
#     "conteact_person ": "張增懿",
#     "contact_num": "02-23445280",
#     "email": "chang_ty@cht.com.tw",
#     "recipient": "兆豐國際商業銀行國外部匯兌科",
#     "year": "112",
#     "month": "01",
#     "day": "30",
#     "text_number": "TPE112013001",
#     "topic_bank_name": "CIENA JP",
#     "payment_name": "TPE海纜款項",
#     "chinese_payment": "美金四八、五七六．○○",
#     "arabic_payment": "48,576.00",
#     "account_no_1": "007-53-110022",
#     "account_name": "Ciena Communications Japan Co. Ltd.",
#     "bank": "JPMorgan Chase Bank Luxembourg S.A.",
#     "bank_address": "6 route de Treves, Senningerberg, 2633, Luxembourg",
#     "account_no_2": "6550207141",
#     "iban": "LU290670006550207141",
#     "swift": "CHASLULX",
#     "invoice_num": "Invoice No.15328/15428",
#     "work_title": "TPE UPG#11(BM1/BM2)",
#     "foreign_currency_demand_deposit_no": "007-53-110022",
# }
#
# doc.render(context)
# doc.save("output.docx")

import markdown2

with open("CBP專案/meeting_report_230210.md", "r") as fp:
    content = fp.read()

html = markdown2.markdown(content)

# save html
with open("output.html", "w") as fp:
    fp.write(html)
