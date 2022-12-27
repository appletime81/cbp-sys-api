from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from .engine import Base


class InvoiceWKMasterDBModel(Base):
    __tablename__ = "InvoiceWKMaster"
    """
    WKMasterID  int NOT NULL AUTO_INCREMENT,
    InvoiceNo   varchar(20),
    Description  varchar(128),
    SupplierID  varchar(6),
    SubmarineCable varchar(10),
    WorkTitle   varchar(50),
    ContractType varchar(20),
    IssueDate   datetime,
    InvoiceDueDate datetime,
    PartyID   varchar(6),
    Status   varchar(20),
    IsPro    TINYINT(1),
    IsRecharge  TINYINT(1),
    IsLiability  TINYINT(1),
    TotalAmount  decimal(65,2),
    CreateDate    datetime,
    PRIMARY KEY(WKMasterID)
    """

    WKMasterID = Column(Integer, primary_key=True, index=True)
    InvoiceNo = Column(String(20))
    Description = Column(String(128))
    SupplierID = Column(String(6))
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    ContractType = Column(String(20))
    IssueDate = Column(String(20))
    InvoiceDueDate = Column(String(20))
    PartyID = Column(String(6))
    Status = Column(String(20))
    IsPro = Column(Boolean)
    IsRecharge = Column(Boolean)
    IsLiability = Column(Boolean)
    TotalAmount = Column(Float)
    CreateDate = Column(String(20))


class InvoiceWKDetailDBModel(Base):
    __tablename__ = "InvoiceWKDetail"

    """
    WKDetailID   int NOT NULL AUTO_INCREMENT,
    WKMasterID   int NOT NULL,
    BillMilestone  varchar(20),
    FeeType     varchar(10),
    FeeItem     varchar(100),
    FeeAmount    decimal(65,2),
    PRIMARY KEY(WKDetailID)
    """

    WKDetailID = Column(Integer, primary_key=True, index=True)
    WKMasterID = Column(Integer)
    BillMilestone = Column(String(20))
    FeeType = Column(String(10))
    FeeItem = Column(String(100))
    FeeAmount = Column(Float)


class InvoiceMasterDBModel(Base):
    __tablename__ = "InvoiceMaster"
    """
    InvMasterID   int NOT NULL AUTO_INCREMENT,
    WKMasterID   int,
    InvoiceNo    varchar(20),
    PartyID       varchar(6),
    SupplyID    varchar(6),
    SubmarineCable varchar(10),
    ContractType  varchar(20),
    IssueDate    datetime,
    InvoiceDueDate datetime,
    Status     varchar(20),
    PRIMARY KEY(InvMasterID)
    """

    InvMasterID = Column(Integer, primary_key=True, index=True)
    WKMasterID = Column(Integer)
    InvoiceNo = Column(String(20))
    PartyID = Column(String(6))
    SupplyID = Column(String(6))
    SubmarineCable = Column(String(10))
    ContractType = Column(String(20))
    IssueDate = Column(String(20))
    InvoiceDueDate = Column(String(20))
    Status = Column(String(20))


class InvoiceDetailDBModel(Base):
    __tablename__ = "InvoiceDetail"
    """
    InvDetailID  int NOT NULL AUTO_INCREMENT,
    InvMasterID   int NOT NULL,
    FeeItem     varchar(100),
    FeeAmountPre   decimal(12,2),
    Liability       decimal(13,10),
    FeeAmountPost   decimal(12,2),
    Difference      decimal(3,2),
    PRIMARY KEY(InvDetailID)
    """

    InvDetailID = Column(Integer, primary_key=True, index=True)
    InvMasterID = Column(Integer)
    FeeItem = Column(String(100))
    FeeAmountPre = Column(Float)
    Liability = Column(Float)
    FeeAmountPost = Column(Float)
    Difference = Column(Float)
