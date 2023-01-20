from fastapi import APIRouter, Request, status, Depends, Body
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import orm_to_pydantic
from copy import deepcopy

router = APIRouter()


# ------------------------------ Liability ------------------------------
# 查詢Liability
@router.get("/Liability/{LiabilityCondition}")
async def getLiability(
    request: Request,
    LiabilityCondition: str,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, LiabilityDBModel)
    table_name = "Liability"
    if LiabilityCondition == "all":
        LiabilityDataList = crud.get_all()
    elif "start" in LiabilityCondition or "end" in LiabilityCondition:
        LiabilityCondition = convert_url_condition_to_dict(LiabilityCondition)
        sql_condition = convert_dict_to_sql_condition(LiabilityCondition, table_name)
        LiabilityDataList = crud.get_all_by_sql(sql_condition)
    else:
        LiabilityCondition = convert_url_condition_to_dict(LiabilityCondition)
        LiabilityDataList = crud.get_with_condition(LiabilityCondition)
    return LiabilityDataList


@router.post("/addLiability", status_code=status.HTTP_201_CREATED)
async def addLiability(
    request: Request,
    LiabilityPydanticData: LiabilitySchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, LiabilityDBModel)

    # give CreateDate
    LiabilityPydanticData.CreateDate = convert_time_to_str(datetime.now())

    # add into database
    crud.create(LiabilityPydanticData)
    return {"message": "Liability successfully created"}


@router.post("/updateLiability")
async def updateLiability(
    request: Request,
    db: Session = Depends(get_db),
):
    LiabilityDictData = await request.json()
    LBRawID = LiabilityDictData.get("LBRawID")
    crud = CRUD(db, LiabilityDBModel)
    LiabilityDataList = crud.get_with_condition({"LBRawID": LBRawID})
    for LiabilityData in LiabilityDataList:
        crud.update(LiabilityData, LiabilityDictData)
    return {"message": "Liability successfully updated"}


@router.post("/deleteLiability")
async def deleteLiability(
    request: Request,
    db: Session = Depends(get_db),
):
    LiabilityDictData = await request.json()
    LBRawID = LiabilityDictData.get("LBRawID")
    crud = CRUD(db, LiabilityDBModel)
    crud.remove(LBRawID)
    return {"message": "Liability successfully deleted"}


# for dropdown list
@router.get("/dropdownmenuParties")
async def getDropdownMenuParties(
    request: Request,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, LiabilityDBModel)
    LiabilityDataList = crud.get_all()
    PartyNameList = []
    for LiabilityData in LiabilityDataList:
        PartyNameList.append(LiabilityData.PartyName)
    PartyNameList = list(set(PartyNameList))
    return PartyNameList




# -----------------------------------------------------------------------
