import os
import io
import json
import uuid
import copy
from pprint import pprint

# import utils
from utils.utils import convert_time_to_str

# schemas (pydantic models)
from schemas import *

# database
from database.engine import *
from database.models import *

# crud
from crud import *

# pydantic and orm converters
from utils.orm_pydantic_convert import orm_to_pydantic, pydantic_to_orm

from fastapi.responses import Response
from datetime import timedelta, datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, Depends, Request, HTTPException, Body

app = FastAPI()

ROOT_URL = "/api/v1"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------ InvoiceWKMaster and InvoiceWKDetail and InvoiceMaster and InvoiceDetail ------------------------------


@app.post(
    f"{ROOT_URL}/generateInvoiceWKMaster&InvoiceWKDetail&InvoiceMaster&InvoiceDetail"
)
async def generateInvoiceWKMasterInvoiceWKDetailInvoiceMasterInvoiceDetail(
    request: Request,
    invoice_data: dict = Body(...),
    db: Session = Depends(get_db),
):
    # ---------------- handle InvoiceWKMaster ----------------
    InvoiceWKMasterDictData = invoice_data["InvoiceWKMaster"]

    # call f"{ROOT_URL}/InvoiceWKMaster" to create InvoiceWKMaster
    InvoiceWKMasterResponse = await InvoiceWKMaster(
        request=request,
        invoice_wk_master=InvoiceWKMasterDictData,
        db=db,
    )
    # # convert dict to pydantic model
    # InvoiceWKMasterPydanticData = InvoiceWKMasterSchema(**InvoiceWKMasterDictData)

    # # insert data to database
    # create_invoice_wk_master(db, InvoiceWKMasterPydanticData)

    # # get InvoiceWKMasterID
    # justAddedInvoiceWKMaster = get_invoice_wk_master_with_condition(
    #     db, InvoiceWKMasterDictData
    # )
    # WKMasterID = justAddedInvoiceWKMaster.WKMasterID
    # print("WKMasterID: ", WKMasterID)

    # --------------------------------------------------------

    # ---------------- handle InvoiceMaster ----------------
    InvoiceMasterPydanticData = InvoiceMasterSchema(
        WKMasterID=WKMasterID,
        InvoiceNo=InvoiceWKMasterDictData["InvoiceNo"],
        PartyID=InvoiceWKMasterDictData["PartyID"],
        SupplyID=InvoiceWKMasterDictData["SupplyID"],
        SubmarineCable=InvoiceWKMasterDictData["SubmarineCable"],
        ContractType=InvoiceWKMasterDictData["ContractType"],
        IssueDate=InvoiceWKMasterDictData["IssueDate"],
        InvoiceDueDate=InvoiceWKMasterDictData["InvoiceDueDate"],
        Status=InvoiceWKMasterDictData["Status"],
    )

    # insert data to database
    create_invoice_master(db, InvoiceMasterPydanticData)

    # --------------------------------------------------------

    # ---------------- handle InvoiceWKDetail ----------------
    InvoiceWKDetailDictData = invoice_data["InvoiceWKDetail"]

    # generate all complete InvoiceWKDetail data
    for item in InvoiceWKDetailDictData:
        item["WKMasterID"] = WKMasterID

        # convert dict to pydantic model
        InvoiceWKDetailPydanticData = InvoiceWKDetailSchema(**item)

        # convert pydantic model to orm model
        InvoiceWKDetailOrmData = pydantic_to_orm(
            InvoiceWKDetailPydanticData, InvoiceWKDetailDBModel
        )

        # insert data to database
        create_invoice_wk_detail(db, InvoiceWKDetailOrmData)
    # --------------------------------------------------------
    return {"message": "success"}


@app.get(f"{ROOT_URL}/InvoiceWKMaster/" + "{InvoiceWKMasterCondition}")
async def getInvoiceWKMaster(request: Request, InvoiceWKMasterCondition: str, db: Session = Depends(get_db)):
    if InvoiceWKMasterCondition == "all":
        InvoiceWKMasterData = get_all_invoice_wk_master(db)
    return InvoiceWKMasterData


@app.post(f"{ROOT_URL}/InvoiceWKMaster")
async def InvoiceWKMaster(
    request: Request,
    InvoiceWKMasterPydanticData: InvoiceWKMasterSchema,
    db: Session = Depends(get_db),
):
    create_invoice_wk_master(db, InvoiceWKMasterPydanticData)

    # convert pydantic model to dict
    InvoiceWKMasterDictData = InvoiceWKMasterPydanticData.dict()

    # get InvoiceWKMasterID
    justAddedInvoiceWKMaster = get_invoice_wk_master_with_condition(
        db, InvoiceWKMasterDictData
    )
    WKMasterID = justAddedInvoiceWKMaster.WKMasterID
    return {"WKMasterID": WKMasterID}


# -------------------------------------------------------------------------------------------------------------------------------------
