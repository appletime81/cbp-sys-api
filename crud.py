from pprint import pprint
from sqlalchemy.orm import Session
from sqlalchemy.orm.sync import update

from database.engine import engine
from database.models import *
from schemas import *
from copy import deepcopy


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
            DueDate=invoice_wk_master.DueDate,
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
            DueDate=invoice_wk_master.DueDate,
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
    db_invoice_master = InvoiceMasterDBModel(**invoice_master.dict())
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
        for k, v in dict_condition.items():
            setattr(item, k, v)
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
    db_invoice_detail = InvoiceDetailDBModel(**invoice_detail.dict())
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
    db_bill_master = BillMasterDBModel(**bill_master.dict())
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
    db_liability = LiabilityDBModel(**liability.dict())
    db.add(db_liability)
    db.commit()
    db.refresh(db_liability)


def update_liability(db: Session, dict_condition: dict):
    pprint(dict_condition)
    db_liability = db.query(LiabilityDBModel).filter_by(
        **{"LBRawID": dict_condition.get("LBRawID")}
    )
    for item in db_liability:
        for k, v in dict_condition.items():
            setattr(item, k, v)
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
        SupplierID=supplier.SupplierID, SupplierName=supplier.SupplierName,
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


class CRUD:
    def __init__(self, db: Session, model, filter_condition: dict):
        self.db = db
        self.model = model
        self.condition = filter_condition

    def get_with_condition(self):
        return self.db.query(self.model).filter_by(**self.filter_condition).all()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, obj_in):
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj, obj_in):
        for field in obj_in:
            setattr(db_obj, field, obj_in[field])
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, id):
        obj = self.db.query(self.model).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
