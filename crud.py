from sqlalchemy.orm import Session
from database.models import (
    InvoiceWKMasterDBModel,
    InvoiceWKDetailDBModel,
    InvoiceMasterDBModel,
    InvoiceDetailDBModel,
)
from schemas import (
    InvoiceWKMasterModel,
    InvoiceWKDetailModel,
    InvoiceMasterModel,
    InvoiceDetailModel,
)

# ------------------------------ InvoiceWKMaster ------------------------------
def create_invoice_wk_master(db: Session, invoice_wk_master: InvoiceWKMasterModel):
    db_invoice_wk_master = InvoiceWKMasterDBModel(
        InvoiceNo=invoice_wk_master.InvoiceNo,
        Description=invoice_wk_master.Description,
        SupplyID=invoice_wk_master.SupplyID,
        SubmarineCable=invoice_wk_master.SubmarineCable,
        WorkTitle=invoice_wk_master.WorkTitle,
        ContractType=invoice_wk_master.ContractType,
        IssueDate=invoice_wk_master.IssueDate,
        InvoiceDueDate=invoice_wk_master.InvoiceDueDate,
        PartyID=invoice_wk_master.PartyID,
        Status=invoice_wk_master.Status,
        IsPro=invoice_wk_master.IsPro,
        IsRecharge=invoice_wk_master.IsRecharge,
        IsLiability=invoice_wk_master.IsLiability,
        TotalAmount=invoice_wk_master.TotalAmount,
    )
    db.add(db_invoice_wk_master)
    db.commit()
    db.refresh(db_invoice_wk_master)


# -----------------------------------------------------------------------------

# ------------------------------ InvoiceWKDetail ------------------------------
def create_invoice_wk_detail(
    db: Session, invoice_wk_detail: InvoiceWKDetailModel
):
    db_invoice_wk_detail = InvoiceWKDetailDBModel(
        WKDetailID=invoice_wk_detail.WKDetailID,
        WKMasterID=invoice_wk_detail.WKMasterID,
        BillMilestone=invoice_wk_detail.BillMilestone,
        FeeType=invoice_wk_detail.FeeType,
        FeeItem=invoice_wk_detail.FeeItem,
        FeeAmount=invoice_wk_detail.FeeAmount,
    )
    db.add(db_invoice_wk_detail)
    db.commit()
    try:
        db.refresh(db_invoice_wk_detail)
    except Exception as e:
        print(e)


# -----------------------------------------------------------------------------
