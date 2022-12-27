from datetime import datetime
from pydantic import BaseModel
from typing import Union, Optional, List, Dict
from bson.objectid import ObjectId


class InvoiceWKMasterSchema(BaseModel):
    """
    WKMasterID   int NOT NULL AUTO_INCREMENT,
    InvoiceNo    varchar(20),
    Description   varchar(128),
    SupplyID    varchar(6),
    SubmarineCable varchar(10),
    WorkTitle    varchar(50),
    ContractType  varchar(20),
    IssueDate    datetime,
    InvoiceDueDate datetime,
    PartyID     varchar(6),
    Status     varchar(20),
    IsPro      TINYINT(1),
    IsRecharge   TINYINT(1),
    IsLiability   TINYINT(1),
    TotalAmount   decimal(65,2),
    PRIMARY KEY(WKMasterID)
    """

    WKMasterID: Optional[int]
    InvoiceNo: str
    Description: str
    SupplierID: str
    SubmarineCable: str
    WorkTitle: str
    ContractType: str
    IssueDate: datetime
    InvoiceDueDate: datetime
    PartyID: str
    Status: str
    IsPro: bool
    IsRecharge: bool
    IsLiability: bool
    TotalAmount: float
    CreateDate: Optional[datetime]

class InvoiceWKDetailSchema(BaseModel):
    """
    WKDetailID   int NOT NULL AUTO_INCREMENT,
    WKMasterID   int NOT NULL,
    BillMilestone  varchar(20),
    FeeType     varchar(10),
    FeeItem     varchar(100),
    FeeAmount    decimal(65,2),
    PRIMARY KEY(WKDetailID)
    """

    WKDetailID: Optional[int]
    WKMasterID: Optional[int]
    BillMilestone: str
    FeeType: Optional[str]
    FeeItem: Optional[str]
    FeeAmount: float


class InvoiceMasterSchema(BaseModel):
    """
    InvMasterID    int NOT NULL AUTO_INCREMENT,
    WKMasterID     int,
    InvoiceNo      varchar(20),
    PartyID        varchar(6),
    SupplyID       varchar(6),
    SubmarineCable varchar(10),
    ContractType   varchar(20),
    IssueDate      datetime,
    InvoiceDueDate datetime,
    Status         varchar(20),
    PRIMARY KEY(InvMasterID)
    """

    InvMasterID: Optional[int]
    WKMasterID: int
    InvoiceNo: str
    PartyID: str
    SupplyID: str
    SubmarineCable: str
    ContractType: str
    IssueDate: datetime
    InvoiceDueDate: datetime
    Status: str


class InvoiceDetailSchema(BaseModel):
    """
    InvDetailID     int NOT NULL AUTO_INCREMENT,
    InvMasterID     int NOT NULL,
    FeeItem         varchar(100),
    FeeAmountPre    decimal(12,2),
    Liability       decimal(13,10),
    FeeAmountPost   decimal(12,2),
    Difference      decimal(3,2),
    PRIMARY KEY(InvDetailID)
    """

    InvDetailID: int
    InvMasterID: int
    FeeItem: str
    FeeAmountPre: float
    Liability: float
    FeeAmountPost: float
    Difference: float
