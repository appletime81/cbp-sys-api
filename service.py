from fastapi import APIRouter, Request, status, Depends
from utils.orm_pydantic_convert import orm_to_pydantic, pydantic_to_orm
from utils.utils import *
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from pprint import pprint

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
async def InvoiceWKMaster(
        request: Request,
        InvoiceWKMasterPydanticData: InvoiceWKMasterSchema,
        db: Session = Depends(get_db),
):
    """
    不須拆帳
     一張 InvoiceWKMaster 對應多張 InvoiceWKDetail
    """
    create_invoice_wk_master(db, InvoiceWKMasterPydanticData)

    # convert pydantic model to dict
    InvoiceWKMasterDictData = InvoiceWKMasterPydanticData.dict()

    pprint(InvoiceWKMasterDictData)
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
@router.post("/InvoiceWKDetail/{WKMasterID}", status_code=status.HTTP_201_CREATED)
async def InvoiceWKDetail(
        request: Request,
        WKMasterID: int,
        InvoiceWKDetailPydanticData: InvoiceWKDetailSchema,
        db: Session = Depends(get_db),
):
    InvoiceWKDetailPydanticData.WKMasterID = WKMasterID
    create_invoice_wk_detail(db, InvoiceWKDetailPydanticData)
    return {"message": "InvoiceWKDetail successfully created"}

# -----------------------------------------------------------------------------

# ------------------------------ Liability ------------------------------
# 查詢Liability
# @router.get("/Liability/{LiabilityCondition}")

# -----------------------------------------------------------------------
