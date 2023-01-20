from fastapi import APIRouter, Request, status, Depends, Body
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import orm_to_pydantic
from copy import deepcopy

router = APIRouter()


# ------------------------------ Suppliers ------------------------------
# 查詢Suppliers
@router.get("/Suppliers/{SuppliersCondition}")
async def getSuppliers(
    request: Request,
    SuppliersCondition: str,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, SuppliersDBModel)
    if SuppliersCondition == "all":
        SuppliersDataList = crud.get_all()
    return SuppliersDataList


@router.post("/Suppliers", status_code=status.HTTP_201_CREATED)
async def addSuppliers(
    request: Request,
    SuppliersPydanticData: SuppliersSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, SuppliersDBModel)
    crud.create(SuppliersPydanticData)
    return {"message": "Supplier successfully created"}


@router.post("/deleteSuppliers")
async def deleteSuppliers(
    request: Request,
    db: Session = Depends(get_db),
):
    query_condition = await request.json()
    SupplierID = query_condition.get("SupplierID")
    crud = CRUD(db, SuppliersDBModel)
    crud.remove(SupplierID)
    return {"message": "Supplier successfully deleted"}


@router.post("/updateSuppliers")
async def updateSuppliers(
    request: Request,
    db: Session = Depends(get_db),
):
    SuppliersDictData = await request.json()
    crud = CRUD(db, SuppliersDBModel)
    SupplierDataList = crud.get_with_condition(
        {"SupplierID": SuppliersDictData.get("SupplierID")}
    )
    for SupplierData in SupplierDataList:
        crud.update(SupplierData, SuppliersDictData)
    return {"message": "Supplier successfully updated"}


# -----------------------------------------------------------------------
