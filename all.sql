CREATE TABLE InvoiceWKMaster
(
    WKMasterID     int NOT NULL AUTO_INCREMENT,
    InvoiceNo      varchar(64),
    SupplierName   varchar(100),
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    ContractType   varchar(20),
    IssueDate      datetime,
    DueDate        datetime,
    PartyName      varchar(100),
    IsPro          tinyint(1),
    IsRecharge     tinyint(1),
    IsLiability    tinyint(1),
    TotalAmount    decimal(12, 2),
    PaidAmount     decimal(12, 2),
    CreateDate     datetime,
    PaidDate       datetime,
    Status         varchar(20),
    PRIMARY KEY (WKMasterID)
);


CREATE TABLE InvoiceWKDetail
(
    WKDetailID     int NOT NULL AUTO_INCREMENT,
    WKMasterID     int NOT NULL,
    InvoiceNo      varchar(64),
    SupplierName   varchar(100),
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    BillMilestone  varchar(20),
    FeeItem        varchar(100),
    FeeAmount      decimal(65, 2),
    PRIMARY KEY (WKDetailID)
);

CREATE TABLE InvoiceMaster
(
    InvMasterID    int NOT NULL AUTO_INCREMENT,
    WKMasterID     int,
    InvoiceNo      varchar(64),
    PartyName      varchar(100),
    SupplierName   varchar(100),
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    ContractType   varchar(20),
    IssueDate      datetime,
    DueDate        datetime,
    IsPro          tinyint(1),
    Status         varchar(20),
    PRIMARY KEY (InvMasterID)
);

CREATE TABLE InvoiceDetail
(
    InvDetailID    int NOT NULL AUTO_INCREMENT,
    InvMasterID    int NOT NULL,
    WKMasterID     int,
    WKDetailID     int,
    InvoiceNo      varchar(64),
    PartyName      varchar(100),
    SupplierName   varchar(100),
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
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
    BillMasterID      int NOT NULL AUTO_INCREMENT,
    BillingNo         varchar(64),
    SubmarineCable    varchar(10),
    WorkTitle         varchar(50),
    PartyName         varchar(100),
    IssueDate         datetime,
    DueDate           datetime,
    FeeAmountSum      decimal(12, 2),
    ReceivedAmountSum decimal(12, 2),
    IsPro             tinyint(1),
    Status            varchar(20),
    PRIMARY KEY (BillMasterID)
);

CREATE TABLE BillDetail
(
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
);

CREATE TABLE CollectStatement
(
    CollectID       int NOT NULL AUTO_INCREMENT,
    BLMasterID      int NOT NULL,
    PartyName       varchar(100),
    SupplierName    varchar(100),
    SubmarineCable  varchar(10),
    WorkTitle       varchar(50),
    BillMilestone   varchar(20),
    FeeItem         varchar(100),
    FeeAmount       decimal(12, 2),
    ReceivedAmount  decimal(12, 2),
    BankFees        decimal(12, 2),
    ShortOverReason varchar(128),
    ReceivedDate    datetime,
    Note            varchar(128),
    Status          varchar(20),
    PRIMARY KEY (CollectID)
);


CREATE TABLE PayMaster
(
    PayMID      int NOT NULL AUTO_INCREMENT,
    SupplierNam varchar(100),
    FeeAmount   decimal(65, 2),
    PaidAmount  decimal(12, 2),
    PaidDate    datetime,
    Note        varchar(128),
    PRIMARY KEY (PayMID)
);


CREATE TABLE PayStatement
(
    PaySID     int NOT NULL AUTO_INCREMENT,
    PayMID     int,
    InvoiceNo  varchar(64),
    FeeAmount  decimal(65, 2),
    PaidAmount decimal(12, 2),
    PaidDate   datetime,
    Note       varchar(128),
    Status     varchar(20),
    PRIMARY KEY (PaySID)
);


CREATE TABLE PayDraft
(
    PayDraftID      int NOT NULL AUTO_INCREMENT,
    SupplierName    varchar(100),
    CableInfo       varchar(64),
    TotalFeeAmount  decimal(12, 2),
    Subject         varchar(128),
    CtactPerson     varchar(10),
    Tel             varchar(20),
    email           varchar(64),
    IssueDate       varchar(32),
    IssueNo         varchar(32),
    OriginalTo      varchar(64),
    CBPBankAcctNo   varchar(20),
    SupBankAcctName varchar(100),
    SupBankName     varchar(100),
    SupBankAddress  varchar(512),
    SupBankAcctNo   varchar(32),
    SupIBAN         varchar(32),
    SupSWIFTCode    varchar(32),
    Status          varchar(20),
    PRIMARY KEY (PayDraftID)
);


CREATE TABLE PayDraftDetail
(
    PayDraftDetailID int NOT NULL AUTO_INCREMENT,
    PayDraftID       int,
    InvoiceNo        varchar(20),
    FeeAmount        varchar(20),
    PRIMARY KEY (PayDraftDetailID)
);


CREATE TABLE Liability
(
    LBRawID        int NOT NULL AUTO_INCREMENT,
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    BillMilestone  varchar(20),
    PartyName      varchar(100),
    LBRatio        decimal(13, 10),
    CreateDate     datetime,
    ModifyNote     varchar(128),
    EndDate        datetime,
    PRIMARY KEY (LBRawID)
);


CREATE TABLE CB
(
    CBID           int NOT NULL AUTO_INCREMENT,
    CBType         varchar(20),
    BillingNo      varchar(64),
    BLDetailID     int,
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    BillMilestone  varchar(20),
    PartyName      varchar(100),
    InvoiceNo      varchar(64),
    CurrAmount     decimal(12, 2),
    CreateDate     datetime,
    LastUpdDate    datetime,
    Note           varchar(128),
    PRIMARY KEY (CBID)
);


CREATE TABLE CBStatement
(
    CBStateID   int NOT NULL AUTO_INCREMENT,
    CBID        int,
    BillingNo   varchar(64),
    BLDetailID  int,
    TransItem   varchar(20),
    OrgAmount   decimal(12, 2),
    TransAmount decimal(12, 2),
    Note        varchar(128),
    CreateDate  datetime,
    PRIMARY KEY (CBStateID)
);


CREATE TABLE CNStatement
(
    CNStateID  int NOT NULL AUTO_INCREMENT,
    CNID       int,
    CBID       int,
    CBType     varchar(20),
    BillingNo  varchar(64),
    InvoiceNo  varchar(64),
    CurrAmount decimal(12, 2),
    IssueDate  datetime,
    DueDate    datetime,
    CBNote     varchar(128),
    PRIMARY KEY (CNStateID)
);


CREATE TABLE CN
(
    CNID       int NOT NULL AUTO_INCREMENT,
    CNNo       varchar(128),
    PartyName  varchar(100),
    CurrAmount decimal(12, 2),
    CreateDate datetime,
    Note       varchar(128),
    PRIMARY KEY (CNID)
);


CREATE TABLE SignRecords
(
    SignID   int NOT NULL AUTO_INCREMENT,
    DocNo    varchar(128),
    DocType  varchar(8),
    SignDate datetime,
    PRIMARY KEY (SignID)
);


CREATE TABLE UndoActions
(
    UndoID  int NOT NULL AUTO_INCREMENT,
    DocNo   varchar(128),
    DocType varchar(8),
    Status  varchar(20),
    Action  varchar(8),
    ExeDate datetime,
    PRIMARY KEY (UndoID)
);


CREATE TABLE Corporates
(
    CorpID         int NOT NULL AUTO_INCREMENT,
    CorpName       varchar(20),
    SubmarineCable varchar(10),
    CreateDate     datetime,
    PRIMARY KEY (CorpID)
);


CREATE TABLE Suppliers
(
    SupplierID   int NOT NULL AUTO_INCREMENT,
    SupplierName varchar(100),
    BankAcctName varchar(100),
    BankAcctNo   varchar(32),
    SWIFTCode    varchar(32),
    IBAN         varchar(32),
    BankName     varchar(100),
    BankAddress  varchar(512),
    PRIMARY KEY (SupplierID)
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


CREATE TABLE Parties
(
    PartyID        int NOT NULL AUTO_INCREMENT,
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    PartyName      varchar(100),
    Address        varchar(512),
    Contact        varchar(20),
    Email          varchar(50),
    Tel            varchar(20),
    PRIMARY KEY (PartyID)
);


CREATE TABLE SubmarineCables
(
    CableID   int NOT NULL AUTO_INCREMENT,
    CableName varchar(64),
    Note      varchar(128),
    PRIMARY KEY (CableID)
);

CREATE TABLE WorkTitles
(
    TitleID int NOT NULL AUTO_INCREMENT,
    Title   varchar(20),
    Note    varchar(128),
    PRIMARY KEY (TitleID)
);

CREATE TABLE ContractTypes
(
    ContractTypeID int NOT NULL AUTO_INCREMENT,
    ContractName   varchar(20),
    Note           varchar(128),
    PRIMARY KEY (ContractTypeID)
);

CREATE TABLE PartiesByContract
(
    ContractID int NOT NULL,
    PartyName  varchar(100),
    PRIMARY KEY (ContractID)
);


CREATE TABLE SuppliersByContract
(
    ContractID   int NOT NULL,
    SupplierName varchar(100),
    PRIMARY KEY (ContractID)
);


CREATE TABLE CBPBankAccount
(
    CorpID    int NOT NULL AUTO_INCREMENT,
    CorpName  varchar(64),
    AcctName  varchar(100),
    AcctNo    varchar(32),
    SWIFTCode varchar(32),
    IBAN      varchar(32),
    Name      varchar(100),
    Address   varchar(512),
    PRIMARY KEY (CorpID)
);


/* --------------------------------------------------------------------- */
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'CHT', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'CMI', 28.5714285714, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'DHT', 3.5714285714, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'Edge', 28.5714285714, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'KDDI', 0.0793650794, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'Singtel', 7.0634920635, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'SKB', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'Telin', 3.5714285714, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'TRUE', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM9a', 'VNPT', 7.1428571429, '2022-12-27 14:30:00', null, null);

insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'CHT', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'CMI', 28.5714285714, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'DHT', 3.5714285714, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'Edge', 28.5714285714, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'KDDI', 0.0793650794, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'Singtel', 7.0634920635, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'SKB', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'Telin', 3.5714285714, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'TRUE', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into Liability (SubmarineCable, WorkTitle, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'Construction', 'BM12', 'VNPT', 7.1428571429, '2022-12-27 14:30:00', null, null);

/*
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'CHT', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'CMI', 28.5714285714, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'DHT', 3.5714285714, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'Edge', 28.5714285714, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'KDDI', 0.0793650794, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'Singtel', 7.0634920635, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'SKB', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'Telin', 3.5714285714, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'TRUE', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SegT', 'BM9b', 'VNPT', 7.1428571429, '2022-12-27 14:30:00', null, null);


insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'CHT', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'CMI', 28.5714285714, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'DHT', 3.5714285714, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'Edge', 28.5714285714, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'KDDI', 0.0793650794, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'Singtel', 7.0634920635, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'SKB', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'Telin', 3.5714285714, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'TRUE', 7.1428571429, '2022-12-27 14:30:00', null, null);
insert into liability (SubmarineCable, BillMilestone, PartyName, LBRatio, CreateDate, ModifyNote, EndDate)
values ('SJC2', 'BM0', 'VNPT', 7.1428571429, '2022-12-27 14:30:00', null, null);