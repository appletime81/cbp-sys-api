# from docxtpl import DocxTemplate
#
# info_dict = {
#     "ContactWindowAndSupervisorInformation": {
#         "Company": "International Business Group,\nChunghwa Telecom Co., Ltd.",
#         "Address": "No. 31, Ai-kuo East Road, Taipei, 106, Taiwan",
#         "Tel": "02-23443897",
#         "Fax": "",
#         "DirectorName": "Hsuan-Lung Liu",
#         "DTel": "+886-2-2344-3912",
#         "DFax": "+886-2-2344-5940",
#         "DEmail": "lsl008@cht.com.tw",
#     },
#     "PartyInformation": {
#         "Company": "SK Broadband Co., Ltd. (SKB)",
#         "Address": "8F, SK Namsan Green Bldg., 24, Toegye-ro, Jung-gu, Seoul 04637, Korea",
#         "Contact": "SUN JIN KUK (Chris)",
#         "Email": "chris.sun@sk.com",
#         "Tel": "+82-10-3702-0461",
#     },
#     "CorporateInformation": {
#         "BankName": "Bank of Taiwan, Hsinyi Branch",
#         "Branch": "",
#         "BranchAddress": "88, Sec. 2, Sinyi Road, Taipei",
#         "BankAcctName": "SJC2 Central Billing Party of Chunghwa Telecom (International Business Group)",
#         "BankAcctNo": "054007501968",
#         "SavingAcctNo": "",
#         "IBAN": "",
#         "SWIFTCode": "BKTWTWTP054",
#         "ACHNo": "",
#         "WireRouting": "",
#         "Address": "31 Aikuo E. Rd., Taipei, Taiwan, 106",
#     },
#     "DetailInformation": [
#         {
#             "Supplier": "NEC Corporation, Submarine Network Division",
#             "InvNumber": "DT0170168-1",
#             "Description": "BM9a Sea cable manufactured (except 8.5km spare cable))- Equipment",
#             "BilledAmount": 1288822.32,
#             "Liability": 7.1428571429,
#             "ShareAmount": 92058.74,
#         },
#         {
#             "Supplier": "NEC Corporation, Submarine Network Division",
#             "InvNumber": "DT0170168-1",
#             "Description": "BM9a Sea cable manufactured (except 8.5km spare cable))- Service",
#             "BilledAmount": 1178227.94,
#             "Liability": 7.1428571429,
#             "ShareAmount": 84159.14,
#         },
#         {
#             "Supplier": "NEC Corporation, Submarine Network Division",
#             "InvNumber": "DT0170168-1",
#             "Description": "BM12 Branching Units (100%)-Equipment",
#             "BilledAmount": 1627300.92,
#             "Liability": 7.1428571429,
#             "ShareAmount": 116235.78,
#         },
#         {
#             "Supplier": "NEC Corporation, Submarine Network Division",
#             "InvNumber": "DT0170168-1",
#             "Description": "BM12 Branching Units (100%)-Service",
#             "BilledAmount": 1487661.54,
#             "Liability": 7.1428571429,
#             "ShareAmount": 106261.54,
#         },
#         {
#             "Supplier": "NEC Corporation, Submarine Network Division",
#             "InvNumber": "CN02CO-KT202304020431",
#             "Description": "BM9a Sea cable manufactured (except 8.5km spare cable))- Equipment",
#             "BilledAmount": -10,
#             "Liability": 100,
#             "ShareAmount": -10,
#         },
#         {
#             "Supplier": "NEC Corporation, Submarine Network Division",
#             "InvNumber": "CN02CO-KT202304020431",
#             "Description": "BM12 Branching Units (100%)-Equipment",
#             "BilledAmount": -10,
#             "Liability": 100,
#             "ShareAmount": -10,
#         },
#         {
#             "Supplier": "NEC Corporation, Submarine Network Division",
#             "InvNumber": "CN02CO-KT202304020431",
#             "Description": "BM12 Branching Units (100%)-Service",
#             "BilledAmount": -10,
#             "Liability": 100,
#             "ShareAmount": -10,
#         },
#     ],
#     "InvoiceNo": "02CO-SK2304020432",
#     "IssueDate": "2021/03/31",
#     "DueDate": "2021/04/30",
# }
#
#
# BillingInfo = info_dict["DetailInformation"]
# for item in BillingInfo:
#     item["BilledAmount"] = "{:.2f}".format(item["BilledAmount"])
#     item["Liability"] = "{:.10f}".format(item["Liability"])
#     item["ShareAmount"] = "{:.2f}".format(item["ShareAmount"])
#
#
# doc = DocxTemplate("bill_draft_tpl.docx")
# context = {
#     "submarinecable": "SJC2",
#     "worktitle": "Construction",
#     "invoicename": "",
#     "PartyCompany": info_dict["PartyInformation"]["Company"],
#     "PartyAddress": info_dict["PartyInformation"]["Address"],
#     "PartyContact": info_dict["PartyInformation"]["Contact"],
#     "PartyEmail": info_dict["PartyInformation"]["Email"],
#     "PartyTel": info_dict["PartyInformation"]["Tel"],
#     "BillingInfo": BillingInfo,
#     "TotalAmount": "{:.2f}".format(sum([float(i["ShareAmount"]) for i in BillingInfo])),
#     "ContactWindowCompany": info_dict["ContactWindowAndSupervisorInformation"][
#         "Company"
#     ],
#     "ContactWindowAddress": info_dict["ContactWindowAndSupervisorInformation"][
#         "Address"
#     ],
#     "ContactWindowTel": info_dict["ContactWindowAndSupervisorInformation"]["Tel"],
#     "ContactWindowFax": info_dict["ContactWindowAndSupervisorInformation"]["Fax"],
#     "ContactWindowDirectorName": info_dict["ContactWindowAndSupervisorInformation"][
#         "DirectorName"
#     ],
#     "ContactWindowDTel": info_dict["ContactWindowAndSupervisorInformation"]["DTel"],
#     "ContactWindowDFax": info_dict["ContactWindowAndSupervisorInformation"]["DFax"],
#     "ContactWindowDEmail": info_dict["ContactWindowAndSupervisorInformation"]["DEmail"],
#     "CorporateBankName": info_dict["CorporateInformation"]["BankName"],
#     "CorporateBranch": info_dict["CorporateInformation"]["Branch"],
#     "CorporateBranchAddress": info_dict["CorporateInformation"]["BranchAddress"],
#     "CorporateBankAcctName": info_dict["CorporateInformation"]["BankAcctName"],
#     "CorporateBankAcctNo": info_dict["CorporateInformation"]["BankAcctNo"],
#     "CorporateSavingAcctNo": info_dict["CorporateInformation"]["SavingAcctNo"],
#     "CorporateSWIFTCode": info_dict["CorporateInformation"]["SWIFTCode"],
#     "IssueDate": info_dict["IssueDate"],
#     "DueDate": info_dict["DueDate"],
#     "InvoiceNo": info_dict["InvoiceNo"],
# }
# doc.render(context)
# doc.save("generated_doc.docx")


# import requests
#
# url = "http://localhost:8000/api/v1/getBillMasterDraftStream"
# headers = {"Content-Type": "application/json"}
# data = {
#     "BillMasterID": 1,
#     "UserID": "chang_ty",
#     "IssueDate": "2023/04/01",
#     "DueDate": "2023/04/30",
#     "WorkTitle": "Construction #11",
#     "InvoiceName": "",
#     "SubmarineCable": "SJC2",
#     "logo": 2,
# }
#
# response = requests.post(url, headers=headers, json=data)
#
# if response.ok:
#     print("User created successfully", response.status_code, response.headers)
# else:
#     print("Failed to create user:", response.status_code, response.text)

import pandas as pd

df = pd.read_csv("LiabilityDataFrameData.csv")
PartyNameList = list(set(df["PartyName"].tolist()))
print(PartyNameList)
