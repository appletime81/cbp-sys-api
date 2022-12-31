from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from .engine import Base


class InvoiceWKMasterDBModel(Base):
    __tablename__ = "InvoiceWKMaster"
    WKMasterID = Column(Integer, primary_key=True, index=True)
    InvoiceNo = Column(String(20))
    Description = Column(String(128))
    SupplierID = Column(String(6))
    SubmarineCable = Column(String(10))
    WorkTitle = Column(String(50))
    ContractType = Column(String(20))
    IssueDate = Column(String(20))
    InvoiceDueDate = Column(String(20))
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
    SupplierID = Column(String(6))
    SubmarineCable = Column(String(10))
    BillMilestone = Column(String(20))
    FeeItem = Column(String(100))
    FeeAmount = Column(Float)


class InvoiceMasterDBModel(Base):
    __tablename__ = "InvoiceMaster"
    InvMasterID = Column(Integer, primary_key=True, index=True)
    WKMasterID = Column(Integer)
    InvoiceNo = Column(String(20))
    PartyName = Column(String(100))
    SupplierID = Column(String(6))
    SubmarineCable = Column(String(10))
    ContractType = Column(String(20))
    IssueDate = Column(String(20))
    InvoiceDueDate = Column(String(20))
    Status = Column(String(20))


class InvoiceDetailDBModel(Base):
    __tablename__ = "InvoiceDetail"
    InvDetailID = Column(Integer, primary_key=True, index=True)
    InvMasterID = Column(Integer)
    WKMasterID = Column(Integer)
    WKDetailID = Column(Integer)
    InvoiceNo = Column(String(20))
    PartyName = Column(String(100))
    SupplierID = Column(String(6))
    SubmarineCable = Column(String(10))
    BillMilestone = Column(String(20))
    FeeItem = Column(String(100))
    FeeAmountPre = Column(Float)
    LBRatio = Column(Float)
    FeeAmountPost = Column(Float)
    Difference = Column(Float)


class LiabilityDBModel(Base):
    __tablename__ = "Liability"
    LiabilityID = Column(Integer, primary_key=True, index=True)
    BillMilestone = Column(String(20))
    PartyName = Column(String(100))
    LBRatio = Column(Float)
    CreateDate = Column(String(20))
    ModifyNote = Column(String(128))
    EndDate = Column(String(20))
