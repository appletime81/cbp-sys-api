from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class InvoiceWKMasterSchema(BaseModel):
    """
    WKMasterID = Column(Integer, primary_key=True, index=True)
    InvoiceNo = Column(String(20))
    SupplierName = Column(String(6))
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    ContractType = Column(String(20))
    IssueDate = Column(String(20))
    DueDate = Column(String(20))
    PartyName = Column(String(100))
    IsPro = Column(Boolean)
    IsRecharge = Column(Boolean)
    IsLiability = Column(Boolean)
    TotalAmount = Column(Float)
    PaidAmount = Column(Float)
    CreateDate = Column(String(20))
    PaidDate = Column(String(20))
    Status = Column(String(20))
    """

    WKMasterID: Optional[int]
    InvoiceNo: str
    SupplierName: str
    SubmarineCable: str
    WorkTitle: str
    ContractType: str
    IssueDate: datetime
    DueDate: datetime
    PartyName: str
    IsPro: bool
    IsRecharge: bool
    IsLiability: bool
    TotalAmount: float
    PaidAmount: Optional[float] = 0.0
    CreateDate: Optional[datetime]
    PaidDate: Optional[datetime]
    Status: str


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
    PONo: Optional[str]
    SupplierName: str
    PartyName: str
    SubmarineCable: str
    WorkTitle: str
    IssueDate: datetime
    DueDate: datetime
    FeeAmountSum: float
    ReceivedAmountSum: float
    IsPro: bool
    Tel: Optional[str]
    Fax: Optional[str]
    TitleInfo: Optional[str]
    URI: Optional[str]
    Status: str


class BillDetailSchema(BaseModel):
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
    ToCBAmount: Optional[float]
    Status: str


class LiabilitySchema(BaseModel):
    LBRawID: Optional[int]
    SubmarineCable: str
    BillMilestone: str
    PartyName: str
    WorkTitle: str
    LBRatio: float
    Note: Optional[str]
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
    CableName: str
    CreateDate: datetime
    AcctName: Optional[str]
    AcctNo: Optional[str]
    SavingAcctNo: Optional[str]
    SWIFTCode: Optional[str]
    IBAN: Optional[str]
    ACHNo: Optional[str]
    WireRouting: Optional[str]
    Name: Optional[str]
    Branch: Optional[str]
    Address: Optional[str]


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
    PartyCode = Column(String(4))
    PartyName = Column(String(100))
    Address = Column(String(512))
    Contact = Column(String(20))
    Email = Column(String(50))
    Tel = Column(String(20))
    BankAcctName = Column(String(100))
    BankAcctNo = Column(String(32))
    SavingAcctNo = Column(String(32))
    SWIFTCode = Column(String(32))
    IBAN = Column(String(32))
    ACHNo = Column(String(32))
    WireRouting = Column(String(32))
    BankName = Column(String(100))
    Branch = Column(String(100))
    BankAddress = Column(String(512))
    """

    PartyID: Optional[int]
    SubmarineCable: Optional[str]
    WorkTitle: Optional[str]
    PartyCode: Optional[str]
    PartyName: Optional[str]
    Address: Optional[str]
    Contact: Optional[str]
    Email: Optional[str]
    Tel: Optional[str]
    BankAcctName: Optional[str]
    BankAcctNo: Optional[str]
    SavingAcctNo: Optional[str]
    SWIFTCode: Optional[str]
    IBAN: Optional[str]
    ACHNo: Optional[str]
    WireRouting: Optional[str]
    BankName: Optional[str]
    Branch: Optional[str]
    BankAddress: Optional[str]


class SubmarineCablesSchema(BaseModel):
    CableID: Optional[int]
    CableCode: Optional[str]
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


class CBIDSchema(BaseModel):
    CBID: int
