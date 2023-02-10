from pprint import pprint
from sqlalchemy.orm import Session
from sqlalchemy.orm.sync import update
from sqlalchemy.sql import func

from database.engine import engine
from database.models import *
from schemas import *
from copy import deepcopy


# ------------------------------ BillMaster ------------------------------
def create_bill_master(db: Session, bill_master: BillMasterSchema):
    db_bill_master = BillMasterDBModel(**bill_master.dict())
    db.add(db_bill_master)
    db.commit()
    db.refresh(db_bill_master)


def get_bill_master_with_condition(db: Session, condition: dict):
    return db.query(BillMasterDBModel).filter_by(**condition).first()


# ------------------------------------------------------------------------


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


class CRUD:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get_with_condition(self, filter_condition: dict):
        return self.db.query(self.model).filter_by(**filter_condition).all()

    def get_all(self):
        return self.db.query(self.model).all()

    def get_all_distinct(self, distinct_field):
        return self.db.query(distinct_field).distinct().all()

    @staticmethod
    def get_all_by_sql(sql: str):
        return engine.execute(sql).all()

    def get_max_id(self, model_id):
        return self.db.query(func.max(model_id)).scalar()

    def create(self, obj_in):
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj, obj_in: dict):
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

    def remove_with_condition(self, condition: dict):
        objs = self.db.query(self.model).filter_by(**condition).all()
        for obj in objs:
            self.db.delete(obj)
            self.db.commit()
