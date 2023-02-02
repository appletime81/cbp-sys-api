from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class InvoiceWKMasterSchema(BaseModel):
    WKMasterID: Optional[int]
    InvoiceNo: Optional[str]
    SupplierName: str
    SubmarineCable: str
    WorkTitle: str
    ContractType: str
    IssueDate: datetime
    DueDate: datetime
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
    WorkTitle: str
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
    WorkTitle: str
    ContractType: str
    IssueDate: datetime
    DueDate: datetime
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
    WorkTitle: str
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


class BillDetailSchema(BaseModel):
    BLDetailID: Optional[int]
    BLMasterID: int
    WKMasterID: int
    InvDetailID: int
    PartyName: str
    SupplierName: str
    SubmarineCable: str
    WorkTitle: str


class LiabilitySchema(BaseModel):
    LBRawID: Optional[int]
    SubmarineCable: str
    BillMilestone: str
    PartyName: str
    WorkTitle: str
    LBRatio: float
    CreateDate: Optional[datetime]
    ModifyNote: Optional[str]
    EndDate: Optional[datetime]


class SuppliersSchema(BaseModel):
    SupplierID: Optional[int]
    SupplierName: str


class CorporatesSchema(BaseModel):
    CorpID: Optional[int]
    CorpName: str
    SubmarineCable: str
    CreateDate: datetime


class ContractsSchema(BaseModel):
    ContractID: Optional[int]
    ContractName: str
    SubmarineCable: str
    WorkTitle: str
    CreateDate: datetime


class PartiesSchema(BaseModel):
    PartyID: Optional[int]
    PartyName: str
    Address: Optional[str]
    Contact: Optional[str]
    Email: Optional[str]
    Tel: Optional[str]


class SubmarineCablesSchema(BaseModel):
    CableID: Optional[int]
    CableName: str
    Note: Optional[str]


class WorkTitlesSchema(BaseModel):
    Title: str
    Note: Optional[str]


class ContractTypesSchema(BaseModel):
    ContractID: Optional[int]
    Note: Optional[str]


class CreditBalanceSchema(BaseModel):
    CBID: Optional[int]
    CBType: str
    BillingNo: str
    BLDetailID: int
    InvoiceNo: str
    CurrAmount: float
    PartyName: str
    CreateDate: datetime
    LastUpDate: datetime
    Note: Optional[str]
