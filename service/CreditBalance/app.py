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
    table_name = "CreditBalance"
    if "generateBillDetail=yes" not in urlCondition:
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
        urlCondition = urlCondition.replace("generateBillDetail=yes", "")
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
    crud.create(CreditBalancePydanticData)
    return {
        "message": "CreditBalance successfully created",
    }
