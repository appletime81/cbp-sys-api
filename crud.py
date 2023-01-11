from pprint import pprint
from sqlalchemy.orm import Session
from database.engine import engine
from database.models import *
from schemas import *


# ------------------------------ InvoiceWKMaster ------------------------------
def create_invoice_wk_master(db: Session, invoice_wk_master: InvoiceWKMasterSchema):
    db_invoice_wk_master = (
        InvoiceWKMasterDBModel(
            InvoiceNo=invoice_wk_master.InvoiceNo,
            Description=invoice_wk_master.Description,
            SupplierName=invoice_wk_master.SupplierName,
            SubmarineCable=invoice_wk_master.SubmarineCable,
            WorkTitle=invoice_wk_master.WorkTitle,
            ContractType=invoice_wk_master.ContractType,
            IssueDate=invoice_wk_master.IssueDate,
            InvoiceDueDate=invoice_wk_master.InvoiceDueDate,
            PartyName=invoice_wk_master.PartyName,
            Status=invoice_wk_master.Status,
            IsPro=invoice_wk_master.IsPro,
            IsRecharge=invoice_wk_master.IsRecharge,
            IsLiability=invoice_wk_master.IsLiability,
            TotalAmount=invoice_wk_master.TotalAmount,
            CreateDate=invoice_wk_master.CreateDate,
        )
        if invoice_wk_master.WKMasterID is None
        else InvoiceWKMasterDBModel(
            WKMasterID=invoice_wk_master.WKMasterID,
            InvoiceNo=invoice_wk_master.InvoiceNo,
            Description=invoice_wk_master.Description,
            SupplierName=invoice_wk_master.SupplierName,
            SubmarineCable=invoice_wk_master.SubmarineCable,
            WorkTitle=invoice_wk_master.WorkTitle,
            ContractType=invoice_wk_master.ContractType,
            IssueDate=invoice_wk_master.IssueDate,
            InvoiceDueDate=invoice_wk_master.InvoiceDueDate,
            PartyName=invoice_wk_master.PartyName,
            Status=invoice_wk_master.Status,
            IsPro=invoice_wk_master.IsPro,
            IsRecharge=invoice_wk_master.IsRecharge,
            IsLiability=invoice_wk_master.IsLiability,
            TotalAmount=invoice_wk_master.TotalAmount,
            CreateDate=invoice_wk_master.CreateDate,
        )
    )
    db.add(db_invoice_wk_master)
    db.commit()
    db.refresh(db_invoice_wk_master)
    return db_invoice_wk_master


def get_all_invoice_wk_master(db: Session):
    return db.query(InvoiceWKMasterDBModel).all()


def get_all_invoice_wk_master_by_sql(sql: str):
    return engine.execute(sql).all()


def get_invoice_wk_master_with_condition(db: Session, condition: dict):
    return db.query(InvoiceWKMasterDBModel).filter_by(**condition).first()


def update_invoice_wk_master(db: Session, dict_condition: dict):
    pprint(dict_condition)
    db_invoice_wk_master = db.query(InvoiceWKMasterDBModel).filter_by(
        **{"WKMasterID": dict_condition.get("WKMasterID")}
    )
    for item in db_invoice_wk_master:
        item.WKMasterID = dict_condition.get("WKMasterID")
        item.InvoiceNo = dict_condition.get("InvoiceNo")
        item.Description = dict_condition.get("Description")
        item.SupplierName = dict_condition.get("SupplierName")
        item.SubmarineCable = dict_condition.get("SubmarineCable")
        item.WorkTitle = dict_condition.get("WorkTitle")
        item.ContractType = dict_condition.get("ContractType")
        item.IssueDate = dict_condition.get("IssueDate")
        item.InvoiceDueDate = dict_condition.get("InvoiceDueDate")
        item.PartyName = dict_condition.get("PartyName")
        item.Status = dict_condition.get("Status")
        item.IsPro = dict_condition.get("IsPro")
        item.IsRecharge = dict_condition.get("IsRecharge")
        item.IsLiability = dict_condition.get("IsLiability")
        item.TotalAmount = dict_condition.get("TotalAmount")
        item.CreateDate = dict_condition.get("CreateDate")
        db.commit()


def delete_invoice_wk_master(db: Session, invoice_wk_master_data: InvoiceMasterDBModel):
    db.delete(invoice_wk_master_data)
    db.commit()


# -----------------------------------------------------------------------------
# ------------------------------ InvoiceWKDetail ------------------------------
def create_invoice_wk_detail(db: Session, invoice_wk_detail: InvoiceWKDetailSchema):
    db_invoice_wk_detail = InvoiceWKDetailDBModel(
        WKDetailID=invoice_wk_detail.WKDetailID,
        WKMasterID=invoice_wk_detail.WKMasterID,
        InvoiceNo=invoice_wk_detail.InvoiceNo,
        SupplierName=invoice_wk_detail.SupplierName,
        SubmarineCable=invoice_wk_detail.SubmarineCable,
        BillMilestone=invoice_wk_detail.BillMilestone,
        FeeItem=invoice_wk_detail.FeeItem,
        FeeAmount=invoice_wk_detail.FeeAmount,
    )
    db.add(db_invoice_wk_detail)
    db.commit()
    try:
        db.refresh(db_invoice_wk_detail)
    except Exception as e:
        print(e)


def get_all_invoice_wk_detail(db: Session):
    return db.query(InvoiceWKDetailDBModel).all()


def get_invoice_wk_detail_with_condition(db: Session, condition: dict):
    return db.query(InvoiceWKDetailDBModel).filter_by(**condition).first()


def get_all_invoice_wk_detail_with_condition(db: Session, condition: dict):
    return db.query(InvoiceWKDetailDBModel).filter_by(**condition).all()


def delete_invoice_wk_detail(
    db: Session, invoice_wk_detail_data: InvoiceWKDetailDBModel
):
    db.delete(invoice_wk_detail_data)
    db.commit()


# -----------------------------------------------------------------------------


# ------------------------------ InvoiceMaster ------------------------------
def create_invoice_master(db: Session, invoice_master: InvoiceMasterSchema):
    db_invoice_master = InvoiceMasterDBModel(
        InvMasterID=invoice_master.InvMasterID,
        WKMasterID=invoice_master.WKMasterID,
        InvoiceNo=invoice_master.InvoiceNo,
        PartyName=invoice_master.PartyName,
        SupplierName=invoice_master.SupplierName,
        SubmarineCable=invoice_master.SubmarineCable,
        ContractType=invoice_master.ContractType,
        IssueDate=invoice_master.IssueDate,
        InvoiceDueDate=invoice_master.InvoiceDueDate,
        Status=invoice_master.Status,
        IsPro=invoice_master.IsPro,
    )
    db.add(db_invoice_master)
    db.commit()
    db.refresh(db_invoice_master)


def get_invoice_master_with_condition(db: Session, condition: dict):
    return db.query(InvoiceMasterDBModel).filter_by(**condition).first()


def get_all_invoice_master(db: Session):
    return db.query(InvoiceMasterDBModel).all()


def get_all_invoice_master_with_condition(db: Session, condition: dict):
    return db.query(InvoiceMasterDBModel).filter_by(**condition).all()


def delete_invoice_master(db: Session, invoice_master_data: InvoiceMasterDBModel):
    db.delete(invoice_master_data)
    db.commit()


def update_invoice_master(db: Session, dict_condition: dict):
    pprint(dict_condition)
    db_invoice_master = db.query(InvoiceMasterDBModel).filter_by(
        **{"WKMasterID": dict_condition.get("WKMasterID")}
    )
    for item in db_invoice_master:
        item.InvMasterID = dict_condition.get("InvMasterID")
        item.WKMasterID = dict_condition.get("WKMasterID")
        item.InvoiceNo = dict_condition.get("InvoiceNo")
        item.PartyName = dict_condition.get("PartyName")
        item.SupplierName = dict_condition.get("SupplierName")
        item.SubmarineCable = dict_condition.get("SubmarineCable")
        item.ContractType = dict_condition.get("ContractType")
        item.IssueDate = dict_condition.get("IssueDate")
        item.InvoiceDueDate = dict_condition.get("InvoiceDueDate")
        item.Status = dict_condition.get("Status")
        db.commit()


def update_invoice_master_status(db: Session, dict_condition: dict):
    pprint(dict_condition)
    db_invoice_master = db.query(InvoiceMasterDBModel).filter_by(
        **{"WKMasterID": dict_condition.get("WKMasterID")}
    )
    for item in db_invoice_master:
        item.Status = dict_condition.get("Status")
        db.commit()


# ---------------------------------------------------------------------------


# ------------------------------ InvoiceDetail ------------------------------
def create_invoice_detail(db: Session, invoice_detail: InvoiceDetailSchema):
    db_invoice_detail = InvoiceDetailDBModel(
        InvMasterID=invoice_detail.InvMasterID,
        WKMasterID=invoice_detail.WKMasterID,
        WKDetailID=invoice_detail.WKDetailID,
        InvoiceNo=invoice_detail.InvoiceNo,
        PartyName=invoice_detail.PartyName,
        SupplierName=invoice_detail.SupplierName,
        SubmarineCable=invoice_detail.SubmarineCable,
        BillMilestone=invoice_detail.BillMilestone,
        FeeItem=invoice_detail.FeeItem,
        FeeAmountPre=invoice_detail.FeeAmountPre,
        LBRatio=invoice_detail.LBRatio,
        FeeAmountPost=invoice_detail.FeeAmountPost,
        Difference=invoice_detail.Difference,
    )
    db.add(db_invoice_detail)
    db.commit()
    db.refresh(db_invoice_detail)


def get_invoice_detail_with_condition(db: Session, condition: dict):
    return db.query(InvoiceDetailDBModel).filter_by(**condition).first()


def get_all_invoice_detail(db: Session):
    return db.query(InvoiceDetailDBModel).all()


def get_all_invoice_detail_with_condition(db: Session, condition: dict):
    return db.query(InvoiceDetailDBModel).filter_by(**condition).all()


def delete_invoice_detail(db: Session, invoice_detail_data: InvoiceDetailDBModel):
    db.delete(invoice_detail_data)
    db.commit()


def get_all_invoice_detail_by_sql(sql: str):
    return engine.execute(sql).all()


# ---------------------------------------------------------------------------

# ------------------------------ BillMaster ------------------------------
def create_bill_master(db: Session, bill_master: BillMasterSchema):
    db_bill_master = BillMasterDBModel(
        BillMasterID=bill_master.BillMasterID,
        BillingNo=bill_master.BillingNo,
        PartyName=bill_master.PartyName,
        CreateDate=bill_master.CreateDate,
        DueDate=bill_master.DueDate,
        Status=bill_master.Status,
        IsPro=bill_master.IsPro,
    )
    db.add(db_bill_master)
    db.commit()
    db.refresh(db_bill_master)


def get_bill_master_with_condition(db: Session, condition: dict):
    return db.query(BillMasterDBModel).filter_by(**condition).first()


# ------------------------------------------------------------------------

# ------------------------------ Liability ------------------------------


def get_liability_with_condition(db: Session, condition: dict):
    return db.query(LiabilityDBModel).filter_by(**condition)


def get_all_liability(db: Session):
    return db.query(LiabilityDBModel).all()


def create_liability(db: Session, liability: LiabilitySchema):
    db_liability = LiabilityDBModel(
        LBRawID=liability.LBRawID,
        BillMilestone=liability.BillMilestone,
        PartyName=liability.PartyName,
        LBRatio=liability.LBRatio,
        CreateDate=liability.CreateDate,
        ModifyNote=liability.ModifyNote,
        EndDate=liability.EndDate,
    )
    db.add(db_liability)
    db.commit()
    db.refresh(db_liability)


def update_liability(db: Session, dict_condition: dict):
    pprint(dict_condition)
    db_liability = db.query(LiabilityDBModel).filter_by(
        **{"LBRawID": dict_condition.get("LBRawID")}
    )
    for item in db_liability:
        item.LBRawID = dict_condition.get("LBRawID")
        item.BillMilestone = dict_condition.get("BillMilestone")
        item.PartyName = dict_condition.get("PartyName")
        item.LBRatio = dict_condition.get("LBRatio")
        item.CreateDate = dict_condition.get("CreateDate")
        item.ModifyNote = dict_condition.get("ModifyNote")
        item.EndDate = dict_condition.get("EndDate")
        db.commit()


def delete_liability(db: Session, dict_condition: dict):
    db_liability = db.query(LiabilityDBModel).filter_by(
        **{"LBRawID": dict_condition.get("LBRawID")}
    )
    for item in db_liability:
        db.delete(item)
        db.commit()


# -----------------------------------------------------------------------

# ------------------------------ Parties ------------------------------
def get_all_party(db: Session):
    return db.query(PartiesDBModel).all()


def create_party(db: Session, party: PartiesSchema):
    db_party = PartiesDBModel(
        PartyName=party.PartyName,
        Address=party.Address,
        Contact=party.Contact,
        Email=party.Email,
        Tel=party.Tel,
    )
    db.add(db_party)
    db.commit()
    db.refresh(db_party)


# ---------------------------------------------------------------------

# ------------------------------ Suppliers ------------------------------
def get_all_supplier(db: Session):
    return db.query(SuppliersDBModel).all()


def create_supplier(db: Session, supplier: SuppliersSchema):
    db_supplier = SuppliersDBModel(
        SupplierID=supplier.SupplierID,
        SupplierName=supplier.SupplierName,
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)


# -----------------------------------------------------------------------

# ------------------------------ Corporates ------------------------------
def get_all_corporate(db: Session):
    return db.query(CorporatesDBModel).all()


def create_corporate(db: Session, corporate: CorporatesSchema):
    db_corporate = CorporatesDBModel(
        CorpID=corporate.CorpID,
        CorpName=corporate.CorpName,
        SubmarineCable=corporate.SubmarineCable,
        CreateDate=corporate.CreateDate,
    )
    db.add(db_corporate)
    db.commit()
    db.refresh(db_corporate)


# ------------------------------------------------------------------------

# ------------------------------ Contracts ------------------------------
def get_all_contract(db: Session):
    return db.query(ContractsDBModel).all()


def create_contract(db: Session, contract: ContractsSchema):
    db_contract = ContractsDBModel(
        ContractID=contract.ContractID,
        ContractName=contract.ContractName,
        SubmarineCable=contract.SubmarineCable,
        WorkTitle=contract.WorkTitle,
        CreateDate=contract.CreateDate,
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)


# -----------------------------------------------------------------------
