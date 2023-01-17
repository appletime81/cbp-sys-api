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
    crud = CRUD(db, InvoiceWKMasterDBModel)
    table_name = "InvoiceWKMaster"
    if InvoiceWKMasterCondition == "all":
        InvoiceWKMasterDataList = crud.get_all()
    elif "start" in InvoiceWKMasterCondition or "end" in InvoiceWKMasterCondition:
        InvoiceWKMasterCondition = convert_url_condition_to_dict(
            InvoiceWKMasterCondition
        )
        sql_condition = convert_dict_to_sql_condition(
            InvoiceWKMasterCondition, table_name
        )

        # get all InvoiceWKMaster by sql
        InvoiceWKMasterDataList = crud.get_all_by_sql(sql_condition)
    else:
        InvoiceWKMasterCondition = convert_url_condition_to_dict(
            InvoiceWKMasterCondition
        )
        InvoiceWKMasterDataList = crud.get_with_condition(InvoiceWKMasterCondition)
    return InvoiceWKMasterDataList


# 新增發票工作主檔
@router.post(f"/InvoiceWKMaster", status_code=status.HTTP_201_CREATED)
async def addInvoiceWKMaster(
    request: Request,
    InvoiceWKMasterPydanticData: InvoiceWKMasterSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, InvoiceWKMasterDBModel)
    crud.create(InvoiceWKMasterPydanticData)
    return {
        "message": "InvoiceWKMaster successfully created",
    }


@router.post(f"/deleteInvoiceWKMaster")
async def deleteInvoiceWKMaster(
    request: Request,
    db: Session = Depends(get_db),
):
    delete_condition = await request.json()
    WKMasterID = delete_condition["WKMasterID"]
    crud = CRUD(db, InvoiceWKMasterDBModel)
    crud.remove(WKMasterID)
    return {"message": "InvoiceWKMaster successfully deleted"}


@router.post(f"/updateInvoiceWKMaster")
async def updateInvoiceWKMasterStatusAndInvoiceMasterStatus(
    request: Request,
    db: Session = Depends(get_db),
):
    update_dict_condition = await request.json()
    crud = CRUD(db, InvoiceWKMasterDBModel)
    InvoiceWKMasterDataList = crud.get_with_condition(
        {"WKMasterID": update_dict_condition["WKMasterID"]}
    )
    for InvoiceWKMasterData in InvoiceWKMasterDataList:
        crud.update(InvoiceWKMasterData, update_dict_condition)

    return {"message": "InvoiceWKMaster status successfully updated"}


# -----------------------------------------------------------------------------

# ------------------------------ InvoiceWKDetail ------------------------------
# 查詢發票工作明細檔
@router.get("/InvoiceWKDetail/{InvoiceWKDetailCondition}")
async def getInvoiceWKDetail(
    request: Request, InvoiceWKDetailCondition: str, db: Session = Depends(get_db)
):
    crud = CRUD(db, InvoiceWKDetailDBModel)
    if InvoiceWKDetailCondition == "all":
        InvoiceWKDetailDataList = crud.get_all()
    else:
        InvoiceWKDetailCondition = convert_url_condition_to_dict(
            InvoiceWKDetailCondition
        )
        InvoiceWKDetailDataList = crud.get_with_condition(InvoiceWKDetailCondition)
    return InvoiceWKDetailDataList


# 新增發票工作明細檔
@router.post("/InvoiceWKDetail", status_code=status.HTTP_201_CREATED)
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
    query_condition = await request.json()
    crud = CRUD(db, InvoiceWKDetailDBModel)
    crud.remove_with_condition(query_condition)
    return {"message": "InvoiceWKDetail successfully deleted"}


# -----------------------------------------------------------------------------

# ------------------------------ InvoiceMaster ------------------------------
# 查詢發票主檔
@router.get("/InvoiceMaster/{InvoiceMasterCondition}")
async def getInvoiceMaster(
    request: Request, InvoiceMasterCondition: str, db: Session = Depends(get_db)
):
    crud = CRUD(db, InvoiceMasterDBModel)
    table_name = "InvoiceMaster"
    if InvoiceMasterCondition == "all":
        InvoiceMasterDataList = crud.get_all()
    elif "start" in InvoiceMasterCondition or "end" in InvoiceMasterCondition:
        InvoiceMasterCondition = convert_url_condition_to_dict(InvoiceMasterCondition)
        sql_condition = convert_dict_to_sql_condition(InvoiceMasterCondition, table_name)

        # get all InvoiceMaster by sql
        InvoiceMasterDataList = crud.get_all_by_sql(sql_condition)
    else:
        InvoiceMasterCondition = convert_url_condition_to_dict(InvoiceMasterCondition)
        InvoiceMasterDataList = crud.get_with_condition(InvoiceMasterCondition)
    return InvoiceMasterDataList


# 新增發票主檔
@router.post("/InvoiceMaster", status_code=status.HTTP_201_CREATED)
async def addInvoiceMaster(
    request: Request,
    InvoiceMasterPydanticData: InvoiceMasterSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, InvoiceMasterDBModel)
    crud.create(InvoiceMasterPydanticData)
    return {
        "message": "InvoiceMaster successfully created",
    }


@router.post("/deleteInvoiceMaster")
async def deleteInvoiceMaster(
    request: Request,
    db: Session = Depends(get_db),
):
    query_condition = await request.json()
    crud = CRUD(db, InvoiceMasterDBModel)
    crud.remove_with_condition(query_condition)
    return {"message": "InvoiceMaster successfully deleted"}


@router.post("/updateInvoiceMaster")
async def updateInvoiceMaster(
    request: Request,
    db: Session = Depends(get_db),
):
    update_dict_condition = await request.json()
    update_dict_condition_copy = deepcopy(update_dict_condition)
    if "Status" in update_dict_condition:
        update_dict_condition.pop("Status")
    crud = CRUD(db, InvoiceMasterDBModel)
    InvoiceMasterDataList = crud.get_with_condition(update_dict_condition)
    for InvoiceMasterData in InvoiceMasterDataList:
        crud.update(InvoiceMasterData, update_dict_condition_copy)
    return {"message": "InvoiceMaster status successfully updated"}


# ---------------------------------------------------------------------------

# ------------------------------ InvoiceDetail ------------------------------
# 建立InvoiceDetail
@router.post("/InvoiceDetail", status_code=status.HTTP_201_CREATED)
async def addInvoiceDetail(
    request: Request,
    InvoiceDetailPydanticData: InvoiceDetailSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, InvoiceDetailDBModel)
    crud.create(InvoiceDetailPydanticData)
    return {
        "message": "InvoiceDetail successfully created",
    }


@router.get("/InvoiceDetail/{InvoiceDetailCondition}")
async def getInvoiceDetail(
    request: Request, InvoiceDetailCondition: str, db: Session = Depends(get_db)
):
    crud = CRUD(db, InvoiceDetailDBModel)
    table_name = "InvoiceDetail"
    if InvoiceDetailCondition == "all":
        InvoiceDetailDataList = crud.get_all()
    elif "start" in InvoiceDetailCondition or "end" in InvoiceDetailCondition:
        InvoiceDetailCondition = convert_url_condition_to_dict(InvoiceDetailCondition)
        sql_condition = convert_dict_to_sql_condition(InvoiceDetailCondition, table_name)
        InvoiceDetailDataList = crud.get_all_by_sql(sql_condition)
    else:
        InvoiceDetailConditionDict = convert_url_condition_to_dict(
            InvoiceDetailCondition
        )
        InvoiceDetailDataList = crud.get_with_condition(InvoiceDetailConditionDict)
    return InvoiceDetailDataList


@router.post("/deleteInvoiceDetail")
async def deleteInvoiceDetail(
    request: Request,
    db: Session = Depends(get_db),
):
    query_condition = await request.json()
    crud = CRUD(db, InvoiceDetailDBModel)
    crud.remove_with_condition(query_condition)
    return {"message": "InvoiceDetail successfully deleted"}


# ---------------------------------------------------------------------------

# ------------------------------ BillMaster ------------------------------
@router.post("/BillMaster", status_code=status.HTTP_201_CREATED)
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
    db: Session = Depends(get_db),
):
    LiabilityDictData = await request.json()
    crud = CRUD(db, LiabilityDBModel)
    crud.create(LiabilityDictData)
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


# -----------------------------------------------------------------------

# ------------------------------ Parties ------------------------------
# 查詢Parties
@router.get("/Parties/{PartiesCondition}")
async def getParties(
    request: Request,
    PartiesCondition: str,
    db: Session = Depends(get_db),
):
    PartiesDataList = []
    if PartiesCondition == "all":
        PartiesDatas = get_all_party(db)
        for PartiesData in PartiesDatas:
            PartiesDataList.append(orm_to_pydantic(PartiesData, PartiesSchema).dict())
    return PartiesDataList


@router.post("/addParties", status_code=status.HTTP_201_CREATED)
async def addParties(
    request: Request,
    db: Session = Depends(get_db),
):
    PartyDictData = await request.json()

    # dict to Pydantic model
    PartyPydanticData = PartiesSchema(**PartyDictData)
    create_party(db, PartyPydanticData)

    return {"message": "Party successfully created"}


# ---------------------------------------------------------------------

# ------------------------------ Suppliers ------------------------------
# 查詢Suppliers
@router.get("/Suppliers/{SuppliersCondition}")
async def getSuppliers(
    request: Request,
    SuppliersCondition: str,
    db: Session = Depends(get_db),
):
    SuppliersDataList = []
    if SuppliersCondition == "all":
        SupplierDatas = get_all_supplier(db)
        for SupplierData in SupplierDatas:
            SuppliersDataList.append(
                orm_to_pydantic(SupplierData, SuppliersSchema).dict()
            )
    return SuppliersDataList


@router.post("/addSuppliers", status_code=status.HTTP_201_CREATED)
async def addSuppliers(
    request: Request,
    db: Session = Depends(get_db),
):
    SupplierDictData = await request.json()

    # dict to Pydantic model
    SupplierPydanticData = SuppliersSchema(**SupplierDictData)

    # add to db
    create_supplier(db, SupplierPydanticData)

    return {"message": "Supplier successfully created"}


# -----------------------------------------------------------------------

# ------------------------------ Corporates ------------------------------
# 查詢Corporates
@router.get("/Corporates/{CorporatesCondition}")
async def getCorporates(
    request: Request,
    CorporatesCondition: str,
    db: Session = Depends(get_db),
):
    CorporatesDataList = []
    if CorporatesCondition == "all":
        CorporateDatas = get_all_corporate(db)
        for CorporateData in CorporateDatas:
            CorporatesDataList.append(
                orm_to_pydantic(CorporateData, CorporatesSchema).dict()
            )
    return CorporatesDataList


@router.post("/addCorporates", status_code=status.HTTP_201_CREATED)
async def addCorporates(
    request: Request,
    db: Session = Depends(get_db),
):
    CorporateDictData = await request.json()

    # dict to Pydantic model
    CorporatePydanticData = CorporatesSchema(**CorporateDictData)

    # add to db
    create_corporate(db, CorporatePydanticData)

    return {"message": "Corporate successfully created"}


# ------------------------------------------------------------------------

# ------------------------------ Contracts ------------------------------
# 查詢Contracts
@router.get("/Contracts/{ContractsCondition}")
async def getContracts(
    request: Request,
    ContractsCondition: str,
    db: Session = Depends(get_db),
):
    ContractsDataList = []
    if ContractsCondition == "all":
        ContractDatas = get_all_contract(db)
        for ContractData in ContractDatas:
            ContractsDataList.append(
                orm_to_pydantic(ContractData, ContractsSchema).dict()
            )
    return ContractsDataList


@router.post("/addContracts", status_code=status.HTTP_201_CREATED)
async def addContracts(
    request: Request,
    db: Session = Depends(get_db),
):
    ContractDictData = await request.json()

    # dict to Pydantic model
    ContractPydanticData = ContractsSchema(**ContractDictData)

    # add to db
    create_contract(db, ContractPydanticData)

    return {"message": "Contract successfully created"}


# -----------------------------------------------------------------------
