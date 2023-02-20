from fastapi import APIRouter, Request, status, Depends
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy

router = APIRouter()


# ------------------------------ CBPBankAccount ------------------------------
# 查詢CBPBankAccount R
@router.get("/CBPBankAccount/{urlCondition}")
async def getCBPBankAccount(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    table_name = "CBPBankAccount"
    crud = CRUD(db, CBPBankAccountDBModel)
    if urlCondition == "all":
        CBPBankAccountDataList = crud.get_all()
    else:
        dictCondition = convert_url_condition_to_dict(urlCondition)
        CBPBankAccountDataList = crud.get_with_condition(dictCondition)
    return CBPBankAccountDataList


# C
@router.post("/CBPBankAccount", status_code=status.HTTP_201_CREATED)
async def addCBPBankAccount(
    request: Request,
    CBPBankAccountPydanticData: CBPBankAccountSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, CBPBankAccountDBModel)
    CBPBankAccountData = crud.create(CBPBankAccountPydanticData)
    return {
        "message": "CBPBankAccount successfully created",
        "CBPBankAccountData": CBPBankAccountData,
    }


# U
@router.post("/updateCBPBankAccount")
async def updateCBPBankAccount(
    request: Request,
    db: Session = Depends(get_db),
):
    CBPBankAccountDictData = await request.json()
    crud = CRUD(db, CBPBankAccountDBModel)
    CBPBankAccountData = crud.get_with_condition(
        {"CorpID": CBPBankAccountDictData["CorpID"]}
    )[0]
    newCBPBankAccountData = crud.update(CBPBankAccountData, CBPBankAccountDictData)
    return {
        "message": "CBPBankAccount successfully updated",
        "newCBPBankAccountData": newCBPBankAccountData,
    }


# D
@router.post("/deleteCBPBankAccount")
async def deleteCBPBankAccount(
    request: Request,
    db: Session = Depends(get_db),
):
    CBPBankAccountDictData = await request.json()
    crud = CRUD(db, CBPBankAccountDBModel)
    crud.remove(CBPBankAccountDictData["CorpID"])
    return {"message": "CBPBankAccount successfully deleted"}
