from datetime import datetime
from pydantic import BaseModel
from typing import Union, Optional, List, Dict
from bson.objectid import ObjectId


class InvoiceWKMasterModel(BaseModel):
    """
    WKMasterID      int NOT NULL AUTO_INCREMENT,
    InvoiceNo       varchar(20),
    Description     varchar(128),
    SupplyID        varchar(6),
    SubmarineCable  varchar(10),
    WorkTitle       varchar(50),
    ContractType    varchar(20),
    IssueDate       datetime,
    InvoiceDueDate  datetime,
    PartyID         varchar(6),
    Status          varchar(20),
    IsPro           TINYINT(1),
    IsRecharge      TINYINT(1),
    IsLiability     TINYINT(1),
    TotalAmount     decimal(65,2),
    PRIMARY KEY(WKMasterID)
    """
    WKMasterID: int
    InvoiceNo: str
    Description: str
    SupplyID: str
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
