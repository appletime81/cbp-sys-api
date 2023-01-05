from fastapi import APIRouter, Request, status, Depends, Body, HTTPException
from utils.orm_pydantic_convert import orm_to_pydantic, pydantic_to_orm
from utils.utils import *
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from pprint import pprint
from typing import Union
from utils.utils import *

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


# -----------------------------------------------------------------------------

# ------------------------------ InvoiceWKDetail ------------------------------
# 查詢發票工作明細檔
@router.get("/InvoiceWKDetail/{InvoiceWKDetailCondition}")
async def getInvoiceWKDetail(
    request: Request, InvoiceWKDetailCondition: str, db: Session = Depends(get_db)
):
    if InvoiceWKDetailCondition == "all":
        InvoiceWKDetailDatas = get_all_invoice_wk_detail(db)
    return InvoiceWKDetailDatas


# 新增發票工作明細檔
@router.post("/InvoiceWKDetail/", status_code=status.HTTP_201_CREATED)
async def addInvoiceWKDetail(
    request: Request,
    InvoiceWKDetailPydanticData: InvoiceWKDetailSchema,
    db: Session = Depends(get_db),
):
    create_invoice_wk_detail(db, InvoiceWKDetailPydanticData)
    InvoiceWKDetailDictData = InvoiceWKDetailPydanticData.dict()
    InvoiceWKDetailDictData.pop("WKDetailID")
    InvoiceWKDetail = get_invoice_wk_detail_with_condition(db, InvoiceWKDetailDictData)
    InvoiceWKDetailDictDataWKDetailID = InvoiceWKDetail.WKDetailID
    return {
        "message": "InvoiceWKDetail successfully created",
        "WKDetailID": InvoiceWKDetailDictDataWKDetailID,
    }


# -----------------------------------------------------------------------------

# ------------------------------ InvoiceMaster ------------------------------
# 查詢發票主檔
@router.get("/InvoiceMaster/{InvoiceMasterCondition}")
async def getInvoiceMaster(
    request: Request, InvoiceMasterCondition: str, db: Session = Depends(get_db)
):
    if InvoiceMasterCondition == "all":
        InvoiceMasterDataList = get_all_invoice_master(db)
    return InvoiceMasterDataList


# 新增發票主檔
@router.post("/InvoiceMaster/", status_code=status.HTTP_201_CREATED)
async def addInvoiceMaster(
    request: Request,
    InvoiceMasterPydanticData: InvoiceMasterSchema,
    db: Session = Depends(get_db),
):
    create_invoice_master(db, InvoiceMasterPydanticData)

    # convert pydantic model to dict
    InvoiceMasterDictData = InvoiceMasterPydanticData.dict()
    InvoiceMasterDictData.pop("InvMasterID")

    # get InvoiceMasterID
    InvoiceMasterData = get_invoice_master_with_condition(db, InvoiceMasterDictData)
    InvoiceMasterId = InvoiceMasterData.InvMasterID
    return {
        "message": "InvoiceMaster successfully created",
        "InvMasterID": InvoiceMasterId,
    }


# ---------------------------------------------------------------------------

# ------------------------------ InvoiceDetail ------------------------------
# 建立InvoiceDetail
@router.post("/InvoiceDetail/", status_code=status.HTTP_201_CREATED)
async def addInvoiceDetail(
    request: Request,
    InvoiceDetailPydanticData: InvoiceDetailSchema,
    db: Session = Depends(get_db),
):
    create_invoice_detail(db, InvoiceDetailPydanticData)

    # get insert data's ID
    InvoiceDetailDictData = InvoiceDetailPydanticData.dict()
    InvoiceDetailDictData.pop("InvDetailID")
    InvDetailID = get_invoice_detail_with_condition(
        db, InvoiceDetailDictData
    ).InvDetailID
    return {
        "message": "InvoiceDetail successfully created",
        "InvDetailID": InvDetailID,
    }


@router.get("/InvoiceDetail/{InvoiceDetailCondition}")
async def getInvoiceDetail(
    request: Request, InvoiceDetailCondition: str, db: Session = Depends(get_db)
):
    if InvoiceDetailCondition == "all":
        InvoiceDetailDataList = get_all_invoice_detail_with_condition(db)
    else:
        InvoiceDetailConditionDict = convert_url_condition_to_dict(InvoiceDetailCondition)
        InvoiceDetailDataList = get_invoice_detail_with_condition(
            db, InvoiceDetailConditionDict
        )
    return InvoiceDetailDataList


# ---------------------------------------------------------------------------

# ------------------------------ Liability ------------------------------
# 查詢Liability
@router.get("/Liability/{LiabilityCondition}")
async def getLiability(
    request: Request,
    LiabilityCondition: str,
    db: Session = Depends(get_db),
):
    LiabilityConditionDict = convert_url_condition_to_dict(LiabilityCondition)
    LiabilityDatas = get_liability_with_condition(db, LiabilityConditionDict)
    return LiabilityDatas


# -----------------------------------------------------------------------
