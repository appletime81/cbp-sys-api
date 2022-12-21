from datetime import datetime
from pydantic import BaseModel
from typing import Union, Optional, List, Dict
from bson.objectid import ObjectId


class InvoiceWKMasterModel(BaseModel):
    """
    WKMasterID   int NOT NULL AUTO_INCREMENT,
    InvoiceNo    varchar(20),
    Description   varchar(128),
    SupplyID    varchar(6),
    SubmarineCable varchar(10),
    WorkTitle    varchar(50),
    ContractType  varchar(20),
    IssueDate    datetime,
    InvoiceDueDate datetime,
    PartyID     varchar(6),
    Status     varchar(20),
    IsPro      TINYINT(1),
    IsRecharge   TINYINT(1),
    IsLiability   TINYINT(1),
    TotalAmount   decimal(65,2),
    PRIMARY KEY(WKMasterID)
    """

    WKMasterID: int
    InvoiceNo: str
    Description: str
    SupplyID: str
    SubmarineCable: str
    WorkTitle: str
    ContractType: str
    IssueDate: datetime
    InvoiceDueDate: datetime
    PartyID: str
    Status: str
    IsPro: bool
    IsRecharge: bool
    IsLiability: bool
    TotalAmount: float


class InvoiceWKDetailModel(BaseModel):
    """
    WKDetailID   int NOT NULL AUTO_INCREMENT,
    WKMasterID   int NOT NULL,
    BillMilestone  varchar(20),
    FeeType     varchar(10),
    FeeItem     varchar(100),
    FeeAmount    decimal(65,2),
    PRIMARY KEY(WKDetailID)
    """

    WKDetailID: int
    WKMasterID: int
    BillMilestone: str
    FeeType: str
    FeeItem: str
    FeeAmount: float


class InvoiceMasterModel(BaseModel):
    """
    InvMasterID    int NOT NULL AUTO_INCREMENT,
    WKMasterID     int,
    InvoiceNo      varchar(20),
    PartyID        varchar(6),
    SupplyID       varchar(6),
    SubmarineCable varchar(10),
    ContractType   varchar(20),
    IssueDate      datetime,
    InvoiceDueDate datetime,
    Status         varchar(20),
    PRIMARY KEY(InvMasterID)
    """

    InvMasterID: int
    WKMasterID: int
    InvoiceNo: str
    PartyID: str
    SupplyID: str
    SubmarineCable: str
    ContractType: str
    IssueDate: datetime
    InvoiceDueDate: datetime
    Status: str


class InvoiceDetailModel(BaseModel):
    """
    InvDetailID     int NOT NULL AUTO_INCREMENT,
    InvMasterID     int NOT NULL,
    FeeItem         varchar(100),
    FeeAmountPre    decimal(12,2),
    Liability       decimal(13,10),
    FeeAmountPost   decimal(12,2),
    Difference      decimal(3,2),
    PRIMARY KEY(InvDetailID)
    """

    InvDetailID: int
    InvMasterID: int
    FeeItem: str
    FeeAmountPre: float
    Liability: float
    FeeAmountPost: float
    Difference: float


class InvoiceWKMasterInvoiceWKDetailInvoiceMasterInvoiceDetailModel(BaseModel):
    '''
    {
        "InvoiceWKMaster":
            {
                "InvoiceNo": "發票號碼",
                "Description": "空值",
                "SupplyID": "供應商",
                "SubmarineCable": "海纜名稱",
                "WorkTitle": "海纜作業",
                "ContractType": "合約種類",
                "IssueDate": "發票日期(datetime)",
                "InvoiceDueDate": "發票到期日(datetime)",
                "PartyID": "會員代號(是否須分攤: 1.否->要填, 2. 是->空值)",
                "Status": "新增發票->暫存(TEMP)，回傳字串TEMP",
                "IsPro": "是否為Pro-forma(bool)",
                "IsRecharge": "是否為短繳補收(bool)",
                "IsLiability": "是否需攤分(bool)",
                "TotalAmount": "總金額(float)"
            },
        "InvoiceWKDetail":
            [
                {
                    "BillMilestone": "記帳段號",
                    "FeeType": "收費種類",
                    "FeeAmount": "費用金額(float)"
                },
                {
                    "BillMilestone": "記帳段號",
                    "FeeType": "收費種類",
                    "FeeAmount": "費用金額(float)"
                }
            ]

    }
    '''

    InvoiceWKMaster: InvoiceWKMasterModel
    InvoiceWKDetail: List[InvoiceWKDetailModel]
