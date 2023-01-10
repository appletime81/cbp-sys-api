from datetime import datetime
from pydantic import BaseModel
from typing import Union, Optional, List, Dict
from bson.objectid import ObjectId


class InvoiceWKMasterSchema(BaseModel):
    WKMasterID: Optional[int]
    InvoiceNo: str
    Description: str
    SupplierName: str
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
    SupplierName: str
    SubmarineCable: str
    BillMilestone: str
    FeeItem: Optional[str]
    FeeAmount: float


class InvoiceMasterSchema(BaseModel):
    InvMasterID: Optional[int]
    WKMasterID: int
    InvoiceNo: str
    PartyName: str
    SupplierName: str
    SubmarineCable: str
    ContractType: str
    IssueDate: datetime
    InvoiceDueDate: datetime
    Status: str
    IsPro: bool


class InvoiceDetailSchema(BaseModel):
    InvDetailID: Optional[int]
    InvMasterID: int
    WKMasterID: int
    WKDetailID: int
    InvoiceNo: str
    PartyName: str
    SupplierName: str
    SubmarineCable: str
    BillMilestone: str
    FeeItem: str
    FeeAmountPre: float
    LBRatio: float
    FeeAmountPost: float
    Difference: float


class BillMasterSchema(BaseModel):
    BillMasterID: Optional[int]
    BillingNo: str
    PartyName: str
    CreateDate: datetime
    DueDate: Optional[datetime]
    Status: str
    IsPro: bool


class LiabilitySchema(BaseModel):
    LBRawID: int
    BillMilestone: str
    PartyName: str
    LBRatio: float
    CreateDate: datetime
    ModifyNote: str
    EndDate: datetime
