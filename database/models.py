from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from .engine import Base


class InvoiceWKMasterDBModel(Base):
    __tablename__ = "InvoiceWKMaster"
    WKMasterID = Column(Integer, primary_key=True, index=True)
    InvoiceNo = Column(String(20))
    SupplierName = Column(String(6))
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    ContractType = Column(String(20))
    IssueDate = Column(String(20))
    DueDate = Column(String(20))
    PartyName = Column(String(100))
    Status = Column(String(20))
    IsPro = Column(Boolean)
    IsRecharge = Column(Boolean)
    IsLiability = Column(Boolean)
    TotalAmount = Column(Float)
    CreateDate = Column(String(20))


class InvoiceWKDetailDBModel(Base):
    __tablename__ = "InvoiceWKDetail"
    WKDetailID = Column(Integer, primary_key=True, index=True)
    WKMasterID = Column(Integer)
    InvoiceNo = Column(String(20))
    SupplierName = Column(String(6))
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    BillMilestone = Column(String(20))
    FeeItem = Column(String(100))
    FeeAmount = Column(Float)


class InvoiceMasterDBModel(Base):
    __tablename__ = "InvoiceMaster"
    InvMasterID = Column(Integer, primary_key=True, index=True)
    WKMasterID = Column(Integer)
    InvoiceNo = Column(String(20))
    PartyName = Column(String(100))
    SupplierName = Column(String(6))
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    ContractType = Column(String(20))
    IssueDate = Column(String(20))
    DueDate = Column(String(20))
    Status = Column(String(20))
    IsPro = Column(Boolean)


class InvoiceDetailDBModel(Base):
    __tablename__ = "InvoiceDetail"
    InvDetailID = Column(Integer, primary_key=True, index=True)
    InvMasterID = Column(Integer)
    WKMasterID = Column(Integer)
    WKDetailID = Column(Integer)
    InvoiceNo = Column(String(20))
    PartyName = Column(String(100))
    SupplierName = Column(String(100.0))
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    BillMilestone = Column(String(20))
    FeeItem = Column(String(100))
    FeeAmountPre = Column(Float)
    LBRatio = Column(Float)
    FeeAmountPost = Column(Float)
    Difference = Column(Float)


class BillMasterDBModel(Base):
    """
    BillMasterID      int NOT NULL AUTO_INCREMENT,
    BillingNo         varchar(64),
    PartyName         varchar(100),
    CreateDate        datetime,
    IssueDate         datetime,
    DueDate           datetime,
    FeeAmountSum      decimal(12, 2),
    ReceivedAmountSum decimal(12, 2),
    IsPro             TINYINT(1),
    Status            varchar(20),
    PRIMARY KEY (BillMasterID)
    """

    __tablename__ = "BillMaster"
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


class BillDetailDBModel(Base):
    """
    BillDetailID    int NOT NULL AUTO_INCREMENT,
    BillMasterID    int NOT NULL,
    WKMasterID      int,
    InvDetailID     int,
    PartyName       varchar(100),
    SupplierName    varchar(100),
    SubmarineCable  varchar(10),
    WorkTitle       varchar(50),
    BillMilestone   varchar(20),
    FeeItem         varchar(100),
    OrgFeeAmount    decimal(12, 2),
    DedAmount       decimal(12, 2),
    FeeAmount       decimal(12, 2),
    ReceivedAmount  decimal(12, 2),
    OverAmount      decimal(12, 2),
    ShortAmount     decimal(12, 2),
    BankFees        decimal(12, 2),
    ShortOverReason varchar(128),
    WriteOffDate    datetime,
    ReceiveDate     datetime,
    Note            varchar(128),
    ToCB            varchar(10),
    Status          varchar(20),
    PRIMARY KEY (BillDetailID)
    """

    __tablename__ = "BillDetail"
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


class LiabilityDBModel(Base):
    __tablename__ = "Liability"
    LBRawID = Column(Integer, primary_key=True, index=True)
    SubmarineCable = Column(String(10))
    BillMilestone = Column(String(20))
    WorkTitle = Column(String(50))
    PartyName = Column(String(100))
    LBRatio = Column(Float)
    CreateDate = Column(String(20))
    ModifyNote = Column(String(128))
    EndDate = Column(String(20))


class PartiesDBModel(Base):
    __tablename__ = "Parties"
    PartyID = Column(Integer, primary_key=True, index=True)
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    PartyName = Column(String(100))
    Address = Column(String(512))
    Contact = Column(String(20))
    Email = Column(String(50))
    Tel = Column(String(20))


class SuppliersDBModel(Base):
    __tablename__ = "Suppliers"
    SupplierID = Column(Integer, primary_key=True, index=True)
    SupplierName = Column(String(100))
    BankAcctName = Column(String(100))
    BankAcctNo = Column(String(32))
    SWIFTCode = Column(String(32))
    IBAN = Column(String(32))
    BankName = Column(String(100))
    BankAddress = Column(String(512))


class CorporatesDBModel(Base):
    __tablename__ = "Corporates"
    CorpID = Column(Integer, primary_key=True, index=True)
    CorpName = Column(String(20))
    SubmarineCable = Column(String(20))
    CreateDate = Column(String(20))


class ContractsDBModel(Base):
    __tablename__ = "Contracts"
    ContractID = Column(Integer, primary_key=True, index=True)
    ContractName = Column(String(20))
    SubmarineCable = Column(String(20))
    WorkTitle = Column(String(20))
    CreateDate = Column(String(20))


class SubmarineCablesDBModel(Base):
    __tablename__ = "SubmarineCables"
    CableID = Column(Integer, primary_key=True, index=True)
    CableName = Column(String(20))
    Note = Column(String(128))


class CreditBalanceDBModel(Base):
    __tablename__ = "CB"
    CBID = Column(Integer, primary_key=True, index=True)
    CBType = Column(String(100))
    BillingNo = Column(String(128))
    BLDetailID = Column(Integer)
    InvoiceNo = Column(String(20))
    CurrAmount = Column(Float)
    PartyName = Column(String(100))
    CreateDate = Column(String(20))
    LastUpDate = Column(String(20))
    Note = Column(String(128))
