from datetime import datetime
from pydantic import BaseModel
from typing import Union, Optional, List, Dict
from bson.objectid import ObjectId


class InvoiceWKMasterSchema(BaseModel):
    WKMasterID: Optional[int]
    InvoiceNo: str
    Description: str
    SupplierID: str
    SubmarineCable: str
    WorkTitle: str
    ContractType: str
    IssueDate: datetime
    InvoiceDueDate: datetime
    PartyName: str
    Status: str
    IsPro: bool
    IsRecharge: bool
    IsLiability: bool
    TotalAmount: float
    CreateDate: Optional[datetime]


class InvoiceWKDetailSchema(BaseModel):
    WKDetailID: Optional[int]
    WKMasterID: Optional[int]
    InvoiceNo: str
    SupplierID: str
    SubmarineCable: str
    BillMilestone: str
    FeeItem: Optional[str]
    FeeAmount: float


class InvoiceMasterSchema(BaseModel):
    InvMasterID: Optional[int]
    WKMasterID: int
    InvoiceNo: str
    PartyName: str
    SupplierID: str
    SubmarineCable: str
    ContractType: str
    IssueDate: datetime
    InvoiceDueDate: datetime
    Status: str


class InvoiceDetailSchema(BaseModel):
    InvDetailID: int
    InvMasterID: int
    WKMasterID: int
    WKDetailID: int
    InvoiceNo: str
    PartyName: str
    SupplierID: str
    SubmarineCable: str
    BillMilestone: str
    FeeItem: str
    FeeAmountPre: float
    LBRatio: float
    FeeAmountPost: float
    Difference: float
