import json

from pprint import pprint

# open json file
with open("test2.json") as f:
    data = json.load(f)


BillDetailDataList = data["BillDetailDataList"]

total_amt = 0
for BillDetailData in BillDetailDataList:
    total_amt += BillDetailData["OrgFeeAmount"]
print(float("{:.2f}".format(total_amt)))
