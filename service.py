from fastapi import APIRouter, Request, status, Depends, Body
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import orm_to_pydantic
from copy import deepcopy

router = APIRouter()


# ------------------------------ InvoiceWKMaster ------------------------------
# 查詢發票工作主檔
@router.get(f"/InvoiceWKMaster/" + "{InvoiceWKMasterCondition}")
async def getInvoiceWKMaster(
    request: Request, InvoiceWKMasterCondition: str, db: Session = Depends(get_db)
):
    table_name = "InvoiceWKMaster"
    if InvoiceWKMasterCondition == "all":
        InvoiceWKMasterData = get_all_invoice_wk_master(db)
    elif "start" in InvoiceWKMasterCondition or "end" in InvoiceWKMasterCondition:
        InvoiceWKMasterCondition = convert_url_condition_to_dict(
            InvoiceWKMasterCondition
        )
        sql_condition = convert_dict_to_sql_condition(
            InvoiceWKMasterCondition, table_name
        )

        # get all InvoiceWKMaster by sql
        InvoiceWKMasterData = get_all_invoice_wk_master_by_sql(sql_condition)
    else:
        InvoiceWKMasterCondition = convert_url_condition_to_dict(
            InvoiceWKMasterCondition
        )
        InvoiceWKMasterData = get_invoice_wk_master_with_condition(
            db, InvoiceWKMasterCondition
        )
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


@router.post(f"/deleteInvoiceWKMaster")
async def deleteInvoiceWKMaster(
    request: Request,
    db: Session = Depends(get_db),
):
    InvoiceWKMasterDBModelData = get_invoice_wk_master_with_condition(
        db, await request.json()
    )
    delete_invoice_wk_master(db, InvoiceWKMasterDBModelData)
    return {"message": "InvoiceWKMaster successfully deleted"}


@router.post(f"/updateInvoiceWKMaster")
async def updateInvoiceWKMaster(
    request: Request,
    invoice_data: dict = Body(...),
    db: Session = Depends(get_db),
):
    # WKMasterID = invoice_data["WKMasterID"]
    deleteInvoiceWKMasterResponse = await deleteInvoiceWKMaster(
        request, deepcopy(invoice_data), db
    )
    return {
        "message": f"{deleteInvoiceWKMasterResponse.get('message')}, InvoiceWKMaster successfully updated"
    }


@router.post(f"/updateInvoiceWKMasterStatus&InvoiceMasterStatus")
async def updateInvoiceWKMasterStatus(
    request: Request,
    db: Session = Depends(get_db),
):

    invoice_data = await request.json()

    # update InvoiceWKMaster status
    update_invoice_wk_master(db, invoice_data)

    # update InvoiceMaster status
    update_invoice_master_condition = {
        "WKMasterID": invoice_data["WKMasterID"],
        "Status": invoice_data["Status"],
    }
    update_invoice_master_status(db, update_invoice_master_condition)

    return {"message": "InvoiceWKMaster status and InvoiceMaster status successfully updated"}


# -----------------------------------------------------------------------------

# ------------------------------ InvoiceWKDetail ------------------------------
# 查詢發票工作明細檔
@router.get("/InvoiceWKDetail/{InvoiceWKDetailCondition}")
async def getInvoiceWKDetail(
    request: Request, InvoiceWKDetailCondition: str, db: Session = Depends(get_db)
):
    if InvoiceWKDetailCondition == "all":
        InvoiceWKDetailDatas = get_all_invoice_wk_detail(db)
    else:
        InvoiceWKDetailCondition = convert_url_condition_to_dict(
            InvoiceWKDetailCondition
        )
        InvoiceWKDetailDatas = get_all_invoice_wk_detail_with_condition(
            db, InvoiceWKDetailCondition
        )
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


@router.post("/deleteInvoiceWKDetail")
async def deleteInvoiceWKDetail(
    request: Request,
    db: Session = Depends(get_db),
):
    InvoiceWKDetailDBModelDataList = get_all_invoice_wk_detail_with_condition(
        db, await request.json()
    )

    for InvoiceWKDetailDBModelData in InvoiceWKDetailDBModelDataList:
        delete_invoice_wk_detail(db, InvoiceWKDetailDBModelData)

    return {"message": "InvoiceWKDetail successfully deleted"}


# -----------------------------------------------------------------------------

# ------------------------------ InvoiceMaster ------------------------------
# 查詢發票主檔
@router.get("/InvoiceMaster/{InvoiceMasterCondition}")
async def getInvoiceMaster(
    request: Request, InvoiceMasterCondition: str, db: Session = Depends(get_db)
):
    if InvoiceMasterCondition == "all":
        InvoiceMasterDataList = get_all_invoice_master(db)
    else:
        InvoiceMasterCondition = convert_url_condition_to_dict(InvoiceMasterCondition)
        InvoiceMasterDataList = get_invoice_master_with_condition(
            db, InvoiceMasterCondition
        )
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


@router.post("/deleteInvoiceMaster")
async def deleteInvoiceMaster(
    request: Request,
    db: Session = Depends(get_db),
):
    InvoiceMasterDBModelDataList = get_all_invoice_master_with_condition(
        db, await request.json()
    )

    for InvoiceMasterDBModelData in InvoiceMasterDBModelDataList:
        delete_invoice_master(db, InvoiceMasterDBModelData)

    return {"message": "InvoiceMaster successfully deleted"}


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
    elif "start" in InvoiceDetailCondition or "end" in InvoiceDetailCondition:
        InvoiceDetailCondition = convert_url_condition_to_dict(InvoiceDetailCondition)
        sql_condition = convert_dict_to_sql_condition(InvoiceDetailCondition)
        InvoiceDetailDataList = get_all_invoice_detail_by_sql(sql_condition)
    else:
        InvoiceDetailConditionDict = convert_url_condition_to_dict(
            InvoiceDetailCondition
        )
        InvoiceDetailDataList = get_all_invoice_detail_with_condition(
            db, InvoiceDetailConditionDict
        )
    return InvoiceDetailDataList


@router.post("/deleteInvoiceDetail")
async def deleteInvoiceDetail(
    request: Request,
    db: Session = Depends(get_db),
):
    InvoiceDetailDBModelDataList = get_all_invoice_detail_with_condition(
        db, await request.json()
    )

    for InvoiceDetailDBModelData in InvoiceDetailDBModelDataList:
        delete_invoice_detail(db, InvoiceDetailDBModelData)

    return {"message": "InvoiceDetail successfully deleted"}


# ---------------------------------------------------------------------------

# ------------------------------ BillMaster ------------------------------
@router.post("/BillMaster/", status_code=status.HTTP_201_CREATED)
async def addBillMaster(
    request: Request,
    BillMasterPydanticData: BillMasterSchema,
    db: Session = Depends(get_db),
):
    create_bill_master(db, BillMasterPydanticData)

    # get insert data's ID
    BillMasterDictData = BillMasterPydanticData.dict()
    BillMasterDictData.pop("BillMasterID")
    BillMasterID = get_bill_master_with_condition(db, BillMasterDictData).BillMasterID
    return {"message": "BillMaster successfully created", "BillMasterID": BillMasterID}


# ------------------------------------------------------------------------

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
