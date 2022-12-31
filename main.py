import os
import io
import json
import uuid
import copy
from pprint import pprint

# import service(業務邏輯)
import service

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
from get_db import get_db

app = FastAPI()

ROOT_URL = "/api/v1"

app.include_router(service.router, prefix=ROOT_URL, tags=["service"])


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

    # IsPro: False, IsLiable: True
    if not InvoiceWKMasterDictData.get("IsPro") and InvoiceWKMasterDictData.get(
        "IsLiability"
    ):
        # 1. create InvoiceWKMaster
        InvoiceWKMasterDictData["CreateDate"] = convert_time_to_str(
            datetime.now()
        )  # add CreateDate
        InvoiceWKMasterPydanticData = InvoiceWKMasterSchema(**InvoiceWKMasterDictData)
        AddInvoiceWKMasterResponse = await service.addInvoiceWKMaster(
            request, InvoiceWKMasterPydanticData, db
        )
        WKMasterID = AddInvoiceWKMasterResponse["WKMasterID"]
        print(f"WKMasterID: {WKMasterID}")

        # 2. create InvoiceWKDetail
        InvoiceWKDetailDictDataList = invoice_data["InvoiceWKDetail"]
        newInvoiceWKDetailDictDataList = []
        for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
            InvoiceWKDetailDictData.update(
                {
                    "WKMasterID": WKMasterID,
                    "InvoiceNo": InvoiceWKMasterDictData["InvoiceNo"],
                    "SupplierID": InvoiceWKMasterDictData["SupplierID"],
                    "SubmarineCable": InvoiceWKMasterDictData["SubmarineCable"],
                }
            )
            newInvoiceWKDetailDictDataList.append(InvoiceWKDetailDictData)
        for InvoiceWKDetailDictData in newInvoiceWKDetailDictDataList:
            InvoiceWKDetailPydanticData = InvoiceWKDetailSchema(
                **InvoiceWKDetailDictData
            )
            AddInvoiceWKDetailResponse = await service.addInvoiceWKDetail(
                request, InvoiceWKDetailPydanticData, db
            )
            print(f"AddInvoiceWKDetailResponse: {AddInvoiceWKDetailResponse}")

        # 3. create InvoiceMaster
        # 3.1 get all BillMilestone, not duplicate
        BillMilestoneList = []
        for InvoiceWKDetailDictData in newInvoiceWKDetailDictDataList:
            BillMilestoneList.append(InvoiceWKDetailDictData["BillMilestone"])
        BillMilestoneList = list(set(BillMilestoneList))

    return {"message": "success"}
