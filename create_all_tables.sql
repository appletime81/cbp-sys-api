DROP TABLE `billmaster`, `invoicedetail`, `invoicemaster`, `invoicewkdetail`, `invoicewkmaster`;

CREATE TABLE InvoiceWKMaster
(
    WKMasterID     int NOT NULL AUTO_INCREMENT,
    InvoiceNo      varchar(20),
    Description    varchar(128),
    SupplierName   varchar(100),
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    ContractType   varchar(20),
    IssueDate      datetime,
    DueDate        datetime,
    PartyName      varchar(100),
    Status         varchar(20),
    IsPro          TINYINT(1),
    IsRecharge     TINYINT(1),
    IsLiability    TINYINT(1),
    TotalAmount    decimal(65, 2),
    CreateDate     datetime,
    PRIMARY KEY (WKMasterID)
);

CREATE TABLE InvoiceWKDetail
(
    WKDetailID     int NOT NULL AUTO_INCREMENT,
    WKMasterID     int NOT NULL,
    InvoiceNo      varchar(20),
    SupplierName   varchar(100),
    SubmarineCable varchar(10),
    BillMilestone  varchar(20),
    FeeItem        varchar(100),
    FeeAmount      decimal(65, 2),
    PRIMARY KEY (WKDetailID)
);

CREATE TABLE InvoiceMaster
(
    InvMasterID    int NOT NULL AUTO_INCREMENT,
    WKMasterID     int,
    InvoiceNo      varchar(20),
    PartyName      varchar(100),
    SupplierName   varchar(100),
    SubmarineCable varchar(10),
    ContractType   varchar(20),
    IssueDate      datetime,
    DueDate        datetime,
    Status         varchar(20),
    IsPro          TINYINT(1),
    PRIMARY KEY (InvMasterID)
);

CREATE TABLE InvoiceDetail
(
    InvDetailID    int NOT NULL AUTO_INCREMENT,
    InvMasterID    int NOT NULL,
    WKMasterID     int,
    WKDetailID     int,
    InvoiceNo      varchar(20),
    PartyName      varchar(100),
    SupplierName   varchar(100),
    SubmarineCable varchar(10),
    BillMilestone  varchar(20),
    FeeItem        varchar(100),
    FeeAmountPre   decimal(12, 2),
    LBRatio        decimal(13, 10),
    FeeAmountPost  decimal(12, 2),
    Difference     decimal(3, 2),
    PRIMARY KEY (InvDetailID)
);

CREATE TABLE BillMaster
(
    BillMasterID int NOT NULL AUTO_INCREMENT,
    BillingNo    varchar(128),
    PartyName    varchar(100),
    CreateDate   datetime,
    DueDate      datetime,
    Status       varchar(20),
    IsPro        TINYINT(1),
    PRIMARY KEY (BillMasterID)
);


CREATE TABLE Liability
(
    LBRawID       int NOT NULL AUTO_INCREMENT,
    BillMilestone varchar(20),
    PartyName     varchar(100),
    LBRatio       decimal(13, 10),
    CreateDate    datetime,
    ModifyNote    varchar(128),
    EndDate       datetime,
    PRIMARY KEY (LBRawID)
);

/* --------------------------------------------------------------------- */
CREATE TABLE Suppliers
(
    SupplierID   int NOT NULL AUTO_INCREMENT,
    SupplierName varchar(100),
    PRIMARY KEY (SupplierID)
);

CREATE TABLE Corporates
(
    CorpID         int NOT NULL AUTO_INCREMENT,
    CorpName       varchar(20),
    SubmarineCable varchar(20),
    CreateDate     datetime,
    PRIMARY KEY (CorpID)
);

CREATE TABLE Parties
(

    PartyName varchar(100) NOT NULL,
    Address   varchar(512),
    Contact   varchar(20),
    Email     varchar(50),
    Tel       varchar(20),
    PRIMARY KEY (PartyName)
);

CREATE TABLE Contracts
(
    ContractID     int NOT NULL AUTO_INCREMENT,
    ContractName   varchar(20),
    SubmarineCable varchar(20),
    WorkTitle      varchar(20),
    CreateDate     datetime,
    PRIMARY KEY (ContractID)
);

CREATE TABLE SubmarineCables
(
    CableID   varchar(20),
    CableName varchar(64),
    Note      varchar(128),
    PRIMARY KEY (CableID)
);

CREATE TABLE WorkTitles
(
    Title varchar(20),
    Note  varchar(128),
    PRIMARY KEY (Title)
);

CREATE TABLE ContractTypes
(
    ContractID varchar(20),
    Note       varchar(128),
    PRIMARY KEY (ContractID)
);

/* --------------------------------------------------------------------- */