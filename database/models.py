from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from .engine import Base


class InvoiceWKMasterDBModel(Base):
    __tablename__ = "InvoiceWKMaster"
    WKMasterID = Column(Integer, primary_key=True, index=True)
    InvoiceNo = Column(String(20))
    Description = Column(String(128))
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
    SupplierName = Column(String(6))
    SubmarineCable = Column(String(10))
    BillMilestone = Column(String(20))
    FeeItem = Column(String(100))
    FeeAmountPre = Column(Float)
    LBRatio = Column(Float)
    FeeAmountPost = Column(Float)
    Difference = Column(Float)


class BillMasterDBModel(Base):
    __tablename__ = "BillMaster"
    BillMasterID = Column(Integer, primary_key=True, index=True)
    BillingNo = Column(String(128))
    PartyName = Column(String(100))
    CreateDate = Column(String(20))
    DueDate = Column(String(20))
    Status = Column(String(20))
    IsPro = Column(Boolean)


class LiabilityDBModel(Base):
    __tablename__ = "Liability"
    LBRawID = Column(Integer, primary_key=True, index=True)
    SubmarineCable = Column(String(10))
    BillMilestone = Column(String(20))
    PartyName = Column(String(100))
    LBRatio = Column(Float)
    CreateDate = Column(String(20))
    ModifyNote = Column(String(128))
    EndDate = Column(String(20))


class PartiesDBModel(Base):
    __tablename__ = "Parties"
    PartyName = Column(String(100), primary_key=True, index=True)
    Address = Column(String(512))
    Contact = Column(String(20))
    Email = Column(String(50))
    Tel = Column(String(20))


class SuppliersDBModel(Base):
    __tablename__ = "Suppliers"
    SupplierID = Column(Integer, primary_key=True, index=True)
    SupplierName = Column(String(100))


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
