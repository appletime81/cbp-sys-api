from sqlalchemy.orm import Session
from database.models import (
    InvoiceWKMasterDBModel,
    InvoiceWKDetailDBModel,
    InvoiceMasterDBModel,
    InvoiceDetailDBModel,
    LiabilityDBModel,
)
from schemas import (
    InvoiceWKMasterSchema,
    InvoiceWKDetailSchema,
    InvoiceMasterSchema,
    InvoiceDetailSchema,
)


# ------------------------------ InvoiceWKMaster ------------------------------
def create_invoice_wk_master(db: Session, invoice_wk_master: InvoiceWKMasterSchema):
    db_invoice_wk_master = InvoiceWKMasterDBModel(
        InvoiceNo=invoice_wk_master.InvoiceNo,
        Description=invoice_wk_master.Description,
        SupplierID=invoice_wk_master.SupplierID,
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
    db.add(db_invoice_wk_master)
    db.commit()
    db.refresh(db_invoice_wk_master)
    return db_invoice_wk_master


def get_all_invoice_wk_master(db: Session):
    return db.query(InvoiceWKMasterDBModel).all()


def get_invoice_wk_master_with_condition(db: Session, condition: dict):
    return db.query(InvoiceWKMasterDBModel).filter_by(**condition).first()


# -----------------------------------------------------------------------------
# ------------------------------ InvoiceWKDetail ------------------------------
def create_invoice_wk_detail(db: Session, invoice_wk_detail: InvoiceWKDetailSchema):
    db_invoice_wk_detail = InvoiceWKDetailDBModel(
        WKDetailID=invoice_wk_detail.WKDetailID,
        WKMasterID=invoice_wk_detail.WKMasterID,
        InvoiceNo=invoice_wk_detail.InvoiceNo,
        SupplierID=invoice_wk_detail.SupplierID,
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


def get_all_invoice_wk_detail(db: Session, condition: dict):
    return db.query(InvoiceWKDetailDBModel).all()


def get_invoice_wk_detail_with_condition(db: Session, condition: dict):
    return db.query(InvoiceWKDetailDBModel).filter_by(**condition).first()


# -----------------------------------------------------------------------------


# ------------------------------ InvoiceMaster ------------------------------
def create_invoice_master(db: Session, invoice_master: InvoiceMasterSchema):
    db_invoice_master = InvoiceMasterDBModel(
        InvMasterID=invoice_master.InvMasterID,
        WKMasterID=invoice_master.WKMasterID,
        InvoiceNo=invoice_master.InvoiceNo,
        PartyName=invoice_master.PartyName,
        SupplierID=invoice_master.SupplierID,
        SubmarineCable=invoice_master.SubmarineCable,
        ContractType=invoice_master.ContractType,
        IssueDate=invoice_master.IssueDate,
        InvoiceDueDate=invoice_master.InvoiceDueDate,
        Status=invoice_master.Status,
    )
    db.add(db_invoice_master)
    db.commit()
    db.refresh(db_invoice_master)


def get_invoice_master_with_condition(db: Session, condition: dict):
    return db.query(InvoiceMasterDBModel).filter_by(**condition).first()


# ---------------------------------------------------------------------------


# ------------------------------ InvoiceDetail ------------------------------
def create_invoice_detail(db: Session, invoice_detail: InvoiceDetailSchema):
    db_invoice_detail = InvoiceDetailDBModel(
        InvMasterID=invoice_detail.InvMasterID,
        WKMasterID=invoice_detail.WKMasterID,
        WKDetailID=invoice_detail.WKDetailID,
        InvoiceNo=invoice_detail.InvoiceNo,
        PartyName=invoice_detail.PartyName,
        SupplierID=invoice_detail.SupplierID,
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


# ---------------------------------------------------------------------------

# ------------------------------ Liability ------------------------------


def get_liability_with_condition(db: Session, condition: dict):
    return db.query(LiabilityDBModel).filter_by(**condition)


# -----------------------------------------------------------------------
