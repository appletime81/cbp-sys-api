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
    """
    BillMasterID = Column(Integer, primary_key=True, index=True)
    BillingNo = Column(String(64))
    PartyName = Column(String(100))
    CreateDate = Column(String(20))
    IssueDate = Column(String(20))
    DueDate = Column(String(20))
    FeeAmountSum = Column(Float)
    ReceivedAmountSum = Column(Float)
    IsPro = Column(Boolean)
    Status = Column(String(20))
    """

    BillMasterID: Optional[int]
    BillingNo: str
    PartyName: str
    CreateDate: datetime
    IssueDate: datetime
    DueDate: datetime
    FeeAmountSum: float
    ReceivedAmountSum: float
    IsPro: bool
    Status: str


class BillDetailSchema(BaseModel):
    """
    BillDetailID = Column(Integer, primary_key=True, index=True)
    BillMasterID = Column(Integer)
    WKMasterID = Column(Integer)
    InvDetailID = Column(Integer)
    PartyName = Column(String(100))
    SupplierName = Column(String(100))
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    BillMilestone = Column(String(20))
    FeeItem = Column(String(100))
    OrgFeeAmount = Column(Float)
    DedAmount = Column(Float)
    FeeAmount = Column(Float)
    ReceivedAmount = Column(Float)
    OverAmount = Column(Float)
    ShortAmount = Column(Float)
    BankFees = Column(Float)
    ShortOverReason = Column(String(128))
    WriteOffDate = Column(String(20))
    ReceiveDate = Column(String(20))
    Note = Column(String(128))
    ToCB = Column(String(10))
    Status = Column(String(20))
    """

    BillDetailID: Optional[int]
    BillMasterID: int
    WKMasterID: int
    InvDetailID: int
    PartyName: str
    SupplierName: str
    SubmarineCable: str
    WorkTitle: str
    BillMilestone: str
    FeeItem: str
    OrgFeeAmount: float
    DedAmount: float
    FeeAmount: float
    ReceivedAmount: float
    OverAmount: float
    ShortAmount: float
    BankFees: float
    ShortOverReason: Optional[str]
    WriteOffDate: Optional[datetime]
    ReceiveDate: Optional[datetime]
    Note: Optional[str]
    ToCB: Optional[str]
    Status: str


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
