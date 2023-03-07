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
    SubmarineCable: str
    WorkTitle: str
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
    ToCBAmount: Optional[str]
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
    """
    SupplierID = Column(Integer, primary_key=True, index=True)
    SupplierName = Column(String(100))
    BankAcctName = Column(String(100))
    BankAcctNo = Column(String(32))
    SWIFTCode = Column(String(32))
    IBAN = Column(String(32))
    BankName = Column(String(100))
    BankAddress = Column(String(512))
    """

    SupplierID: Optional[int]
    SupplierName: Optional[str]
    BankAcctName: Optional[str]
    BankAcctNo: Optional[str]
    SWIFTCode: Optional[str]
    IBAN: Optional[str]
    BankName: Optional[str]
    BankAddress: Optional[str]


class CorporatesSchema(BaseModel):
    CorpID: Optional[int]
    CorpName: str
    SubmarineCable: Optional[str]
    CreateDate: datetime


class ContractsSchema(BaseModel):
    ContractID: Optional[int]
    ContractName: str
    SubmarineCable: str
    WorkTitle: str
    CreateDate: datetime


class PartiesSchema(BaseModel):
    """
    PartyID = Column(Integer, primary_key=True, index=True)
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    PartyName = Column(String(100))
    Address = Column(String(512))
    Contact = Column(String(20))
    Email = Column(String(50))
    Tel = Column(String(20))
    """

    PartyID: Optional[int]
    SubmarineCable: Optional[str]
    WorkTitle: Optional[str]
    PartyName: Optional[str]
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
    """
    CBID           int NOT NULL AUTO_INCREMENT,
    CBType         varchar(20),
    BillingNo      varchar(64),
    BLDetailID     int,
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    InvoiceNo      varchar(64),
    CurrAmount     decimal(12, 2),
    PartyName      varchar(100),
    CreateDate     datetime,
    LastUpdDate    datetime,
    Note           varchar(128),
    PRIMARY KEY (CBID)
    """

    CBID: Optional[int]
    CBType: str
    BillingNo: Optional[str]
    BLDetailID: Optional[int]
    SubmarineCable: str
    WorkTitle: str
    BillMilestone: str
    InvoiceNo: Optional[str]
    CurrAmount: float
    PartyName: str
    CreateDate: datetime
    LastUpdDate: Optional[datetime]
    Note: Optional[str]


class CreditBalanceStatementSchema(BaseModel):
    """
    CBStateID   int NOT NULL AUTO_INCREMENT,
    CBID        int,
    TransItem   varchar(20),
    OrgAmount   decimal(12, 2),
    TransAmount decimal(12, 2),
    Note        varchar(128),
    CreateDate  datetime,
    Oprcode     varchar(6),
    PRIMARY KEY (CBStateID)
    """

    CBStateID: Optional[int]
    CBID: int
    BillingNo: str
    BLDetailID: int
    TransItem: str
    OrgAmount: float
    TransAmount: float
    Note: Optional[str]
    CreateDate: datetime


class PartiesByContractSchema(BaseModel):
    """
    ContractID int NOT NULL,
    PartyName  varchar(100),
    PRIMARY KEY (ContractID)
    """

    ContractID: Optional[int]
    PartyName: str


class CBPBankAccountSchema(BaseModel):
    """
    CorpID    int NOT NULL AUTO_INCREMENT,
    CorpName  varchar(64),
    AcctName  varchar(100),
    AcctNo    varchar(32),
    SWIFTCode varchar(32),
    IBAN      varchar(32),
    Name      varchar(100),
    Address   varchar(512),
    PRIMARY KEY (CorpID)
    """

    CorpID: Optional[int]
    CorpName: Optional[str]
    AcctName: Optional[str]
    AcctNo: Optional[str]
    SWIFTCode: Optional[str]
    IBAN: Optional[str]
    Name: Optional[str]
    Address: Optional[str]


class SuppliersByContractSchema(BaseModel):
    """
    ContractID   int not null,
    SupplierName varchar(100),
    PRIMARY KEY (ContractID)
    """

    ContractID: Optional[int]
    SupplierName: str


class UserSchema(BaseModel):
    """
    CREATE TABLE User
    (
        UserID   int NOT NULL AUTO_INCREMENT,
        UserName varchar(20),
        Password varchar(20),
        CreateDate datetime,
        Note varchar(128),
        PRIMARY KEY (UserID)
    );
    """

    UserID: Optional[int]
    UserName: str
    Password: str
    CreateDate: datetime
    Note: Optional[str]
