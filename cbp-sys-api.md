# 新增發票工作主檔、發票工作明細檔、發票主檔、發票明細檔

## POST http://127.0.0.1:8000/api/v1/generateInvoiceWKMaster&InvoiceWKDetail&InvoiceMaster&InvoiceDetail

### 1. 有Liability

```JSON
{
  "InvoiceWKMaster": {
    "InvoiceNo": "DT0170168-1",
    "Description": "COMMERCIAL INVOICE for SJC2 CABLE SYSTEM[ % of Contract Price=BM9a 3.96%,BM12 5.00% ",
    "SupplierName": "NEC",
    "SubmarineCable": "SJC2",
    "WorkTitle": "Construction",
    "ContractType": "SC",
    "IssueDate": "2022-09-09 00:00:00",
    "InvoiceDueDate": "2022-11-08 00:00:00",
    "PartyName": "",
    "Status": "VALIDATED",
    "IsPro": 0,
    "IsRecharge": 0,
    "IsLiability": 1,
    "TotalAmount": 5582012.72
  },
  "InvoiceWKDetail": [
    {
      "BillMilestone": "BM9a",
      "FeeAmount": 1288822.32,
      "FeeItem": "BM9a Sea cable manufactured (except 8.5km spare cable))- Equipment"
    },
    {
      "BillMilestone": "BM9a",
      "FeeAmount": 1178227.94,
      "FeeItem": "BM9a Sea cable manufactured (except 8.5km spare cable))- Service"
    },
    {
      "BillMilestone": "BM12",
      "FeeAmount": 1627300.92,
      "FeeItem": "BM12 Branching Units (100%)-Equipment"
    },
    {
      "BillMilestone": "BM12",
      "FeeAmount": 1487661.54,
      "FeeItem": "BM12 Branching Units (100%)-Service"
    }
  ]
}
```

### 2. 無Liability

```JSON
{
  "InvoiceWKMaster": {
    "InvoiceNo": "DT0170168-1",
    "Description": "COMMERCIAL INVOICE for SJC2 CABLE SYSTEM[ % of Contract Price=BM9a 3.96%,BM12 5.00% ",
    "SupplierName": "NEC",
    "SubmarineCable": "SJC2",
    "WorkTitle": "Construction",
    "ContractType": "SC",
    "IssueDate": "2022-09-09 00:00:00",
    "InvoiceDueDate": "2022-11-08 00:00:00",
    "PartyName": "CHT",
    "Status": "VALIDATED",
    "IsPro": 0,
    "IsRecharge": 0,
    "IsLiability": 0,
    "TotalAmount": 5582012.72
  },
  "InvoiceWKDetail": [
    {
      "BillMilestone": "BM9a",
      "FeeAmount": 1288822.32,
      "FeeItem": "BM9a Sea cable manufactured (except 8.5km spare cable))- Equipment"
    },
    {
      "BillMilestone": "BM9a",
      "FeeAmount": 1178227.94,
      "FeeItem": "BM9a Sea cable manufactured (except 8.5km spare cable))- Service"
    },
    {
      "BillMilestone": "BM12",
      "FeeAmount": 1627300.92,
      "FeeItem": "BM12 Branching Units (100%)-Equipment"
    },
    {
      "BillMilestone": "BM12",
      "FeeAmount": 1487661.54,
      "FeeItem": "BM12 Branching Units (100%)-Service"
    }
  ]
}
```

---

# 新增帳單主檔

### POST http://127.0.0.1:8000/api/v1/generateBillMaster&BillDetail

```JSON
{
  "WKMasterID": 1,
  "DueDate": "2023-01-23 12:34:56"
}
```