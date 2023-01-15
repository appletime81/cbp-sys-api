import json
from pprint import pprint

# open json file
with open('有Liability_InvoiceDetail結果.json', 'r') as f:
    data = json.load(f)

# print data
pprint(data)
print(len(data))
total_amount = 0
for item in data:
    total_amount += item['FeeAmountPost']
print(total_amount)