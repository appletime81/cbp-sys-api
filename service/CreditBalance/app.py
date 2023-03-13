from fastapi import APIRouter, Request, status, Depends
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy

router = APIRouter()


@router.get("/CreditBalance/{urlCondition}", status_code=status.HTTP_200_OK)
async def getCreditBalance(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, CreditBalanceDBModel)
    table_name = "CB"
    if "getByBillDetail=yes" not in urlCondition:
        if urlCondition == "all":
            CreditBalanceDataList = crud.get_all()
        elif "start" in urlCondition or "end" in urlCondition:
            dictCondition = convert_url_condition_to_dict(urlCondition)
            sql_condition = convert_dict_to_sql_condition(dictCondition, table_name)

            # get all CreditBalance by sql
            CreditBalanceDataList = crud.get_all_by_sql(sql_condition)
        else:
            dictCondition = convert_url_condition_to_dict(urlCondition)
            CreditBalanceDataList = crud.get_with_condition(dictCondition)
    else:
        # urlCondition: SubmarineCable=str&WorkTitle=str&BillMilestone=str&PartyName=str
        urlCondition = urlCondition.replace("getByBillDetail=yes", "")
        dictCondition = convert_url_condition_to_dict(urlCondition)
        CreditBalanceDataList = crud.get_with_condition(dictCondition)
    return CreditBalanceDataList


@router.post("/CreditBalance", status_code=status.HTTP_201_CREATED)
async def addCreditBalance(
    request: Request,
    CreditBalancePydanticData: CreditBalanceSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, CreditBalanceDBModel)
    CreditBalanceDictData = CreditBalancePydanticData.dict()
    CreditBalanceDictData["CreateDate"] = convert_time_to_str(datetime.now())
    CreditBalancePydanticData = CreditBalanceSchema(**CreditBalanceDictData)
    CreditBalanceData = crud.create(CreditBalancePydanticData)
    return {
        "message": "CreditBalance successfully created",
        "CreditBalance": CreditBalanceData,
    }


@router.post("/updateCreditBalance", status_code=status.HTTP_200_OK)
async def updateCreditBalance(
    request: Request,
    db: Session = Depends(get_db),
):
    CBDictData = await request.json()
    crud = CRUD(db, CreditBalanceDBModel)
    CBData = crud.get_with_condition({"CBID": CBDictData["CBID"]})[0]
    newCBData = crud.update(CBData, CBDictData)
    return {"message": "CreditBalance successfully updated", "newCBData": newCBData}
