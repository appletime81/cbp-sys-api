from fastapi import APIRouter, Request, status, Depends
from utils.orm_pydantic_convert import orm_to_pydantic, pydantic_to_orm
from utils.utils import *
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from pprint import pprint
from typing import Union

router = APIRouter()


# ------------------------------ InvoiceWKMaster ------------------------------
# 查詢發票工作主檔
@router.get(f"/InvoiceWKMaster/" + "{InvoiceWKMasterCondition}")
async def getInvoiceWKMaster(
    request: Request, InvoiceWKMasterCondition: str, db: Session = Depends(get_db)
):
    if InvoiceWKMasterCondition == "all":
        InvoiceWKMasterData = get_all_invoice_wk_master(db)
    return InvoiceWKMasterData


# 新增發票工作主檔
@router.post(f"/InvoiceWKMaster", status_code=status.HTTP_201_CREATED)
async def addInvoiceWKMaster(
    request: Request,
    InvoiceWKMasterPydanticData: InvoiceWKMasterSchema,
    db: Session = Depends(get_db),
):
    create_invoice_wk_master(db, InvoiceWKMasterPydanticData)

    # convert pydantic model to dict
    InvoiceWKMasterDictData = InvoiceWKMasterPydanticData.dict()

    # get InvoiceWKMasterID
    InvoiceWKMasterDictData.pop("WKMasterID")  # delete key "WKMasterID"
    justAddedInvoiceWKMaster = get_invoice_wk_master_with_condition(
        db, InvoiceWKMasterDictData
    )
    WKMasterID = justAddedInvoiceWKMaster.WKMasterID
    return {"message": "InvoiceWKMaster successfully created", "WKMasterID": WKMasterID}


# ------------------------------ InvoiceWKDetail ------------------------------
# 查詢發票工作明細檔
@router.get("/InvoiceWKDetail/{InvoiceWKDetailCondition}")
async def getInvoiceWKDetail(
    request: Request, InvoiceWKDetailCondition: str, db: Session = Depends(get_db)
):
    if InvoiceWKDetailCondition == "all":
        InvoiceWKDetailData = get_all_invoice_wk_detail(db)
    return InvoiceWKDetailData


# 新增發票工作明細檔
@router.post("/InvoiceWKDetail/", status_code=status.HTTP_201_CREATED)
async def addInvoiceWKDetail(
    request: Request,
    InvoiceWKDetailPydanticData: InvoiceWKDetailSchema,
    db: Session = Depends(get_db),
):
    create_invoice_wk_detail(db, InvoiceWKDetailPydanticData)
    return {"message": "InvoiceWKDetail successfully created"}


# -----------------------------------------------------------------------------

# ------------------------------ Liability ------------------------------
# 查詢Liability
@router.get("/Liability/{LiabilityCondition}")
async def getLiability(
    request: Request, LiabilityCondition: Union[str, dict], db: Session = Depends(get_db)
):
    if LiabilityCondition == "all" or type(LiabilityCondition) == dict:
        LiabilityData = get_liability_with_condition(db, LiabilityCondition)
    return LiabilityData
# -----------------------------------------------------------------------
