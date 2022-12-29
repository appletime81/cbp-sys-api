# InvoiceWKMaster(發票工作主檔)

```sql
CREATE TABLE InvoiceWKMaster
(
    WKMasterID     int NOT NULL AUTO_INCREMENT,
    InvoiceNo      varchar(20),
    Description    varchar(128),
    SupplierID     varchar(6),
    SubmarineCable varchar(10),
    WorkTitle      varchar(50),
    ContractType   varchar(20),
    IssueDate      datetime,
    InvoiceDueDate datetime,
    PartyName      varchar(100),
    Status         varchar(20),
    IsPro          TINYINT(1),
    IsRecharge     TINYINT(1),
    IsLiability    TINYINT(1),
    TotalAmount    decimal(65, 2),
    CreateD        ate datetime,
    PRIMARY KEY (WKMasterID)
);
```

# InvoiceWKDetail(發票工作明細檔)

```sql
CREATE TABLE InvoiceWKDetail
(
    WKDetailID     int NOT NULL AUTO_INCREMENT,
    WKMasterID     int NOT NULL,
    InvoiceNo      varchar(20),
    PartyName      varchar(100),
    SupplierID     varchar(6),
    SubmarineCable varchar(10),
    BillMilestone  varchar(20),
    FeeItem        varchar(100),
    FeeAmount      decimal(65, 2),
    PRIMARY KEY (WKDetailID)
);
```

# InvoiceMaster(發票主檔)

```sql
CREATE TABLE InvoiceMaster
(
    InvMasterID    int NOT NULL AUTO_INCREMENT,
    WKMasterID     int,
    InvoiceNo      varchar(20),
    PartyName      varchar(100),
    SupplierID     varchar(6),
    SubmarineCable varchar(10),
    ContractType   varchar(20),
    IssueDate      datetime,
    InvoiceDueDate datetime,
    Status         varchar(20),
    IsPro          TINYINT(1),
    PRIMARY KEY (InvMasterID)
);


```

# InvoiceDetail(發票明細檔)

```sql
CREATE TABLE InvoiceDetail
(
    InvDetailID    int NOT NULL AUTO_INCREMENT,
    InvMasterID    int NOT NULL,
    WKMasterID     int,
    WKDetailID     int,
    InvoiceNo      varchar(20),
    PartyName      varchar(100),
    SupplierID     varchar(6),
    SubmarineCable varchar(10),
    BillMilestone  varchar(20),
    FeeItem        varchar(100),
    FeeAmountPre   decimal(12, 2),
    LBRatio        decimal(13, 10),
    FeeAmountPost  decimal(12, 2),
    Difference     decimal(3, 2),
    PRIMARY KEY (InvDetailID)
);


```