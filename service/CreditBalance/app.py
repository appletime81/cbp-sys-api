from fastapi import APIRouter, Request, status, Depends
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import orm_to_pydantic
from copy import deepcopy

router = APIRouter()


@router.get("/CreditBalance/{urlCondition}", status_code=status.HTTP_200_OK)
async def getCreditBalance(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, CreditBalanceDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
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
            urlCondition = convert_url_condition_to_dict(urlCondition)
            CreditBalanceDataList = crud.get_with_condition(urlCondition)
    else:
        # for generate BillDetail("generateBillDetail=yes" in urlCondition)
        # if "generateBillDetail=yes" in urlCondition
        urlCondition = urlCondition.replace("generateBillDetail=yes", "")
        dictCondition = convert_url_condition_to_dict(urlCondition)
        InvoiceDetailDataList = crudInvoiceDetail.get_with_condition(dictCondition)
        InvoiceDetailInvoiceNoList = [
            InvoiceDetailData.InvoiceNo for InvoiceDetailData in InvoiceDetailDataList
        ]
        CreditBalanceDataList = crud.get_value_if_in_a_list(
            CreditBalanceDBModel.InvoiceNo, InvoiceDetailInvoiceNoList
        )

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
