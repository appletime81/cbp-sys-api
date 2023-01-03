import os
import io
import json
import uuid
import copy
from pprint import pprint
from urllib.parse import urlparse

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
        InvoiceMasterDictDataList = []
        for InvoiceWKDetailDictData in newInvoiceWKDetailDictDataList:
            BillMilestoneList.append(InvoiceWKDetailDictData["BillMilestone"])
        BillMilestoneList = list(set(BillMilestoneList))

        # 3.2 get all PartyName, not duplicate
        PartyNameList = []
        for BillMilestone in BillMilestoneList:
            LiabilityDatas = await service.getLiability(
                request, f"BillMilestone={BillMilestone}", db
            )
            for LiabilityData in LiabilityDatas:
                PartyNameList.append(LiabilityData.PartyName)
        PartyNameList = list(set(PartyNameList))
        pprint(PartyNameList)

        # add InvoiceMaster by every PartyName
        for PartyName in PartyNameList:
            InvoiceMasterDictData = {}
            InvoiceMasterDictData.update(
                {
                    "WKMasterID": WKMasterID,
                    "InvoiceNo": InvoiceWKMasterDictData["InvoiceNo"],
                    "PartyName": PartyName,
                    "SupplierID": InvoiceWKMasterDictData["SupplierID"],
                    "ContractType": InvoiceWKMasterDictData["ContractType"],
                    "IssueDate": InvoiceWKMasterDictData["IssueDate"],
                    "InvoiceDueDate": InvoiceWKMasterDictData["InvoiceDueDate"],
                    "SubmarineCable": InvoiceWKMasterDictData["SubmarineCable"],
                    "Status": InvoiceWKMasterDictData["Status"],
                    "IsPro": InvoiceWKMasterDictData["IsPro"],
                }
            )
            InvoiceMasterPydanticData = InvoiceMasterSchema(**InvoiceMasterDictData)
            AddInvoiceMasterResponse = await service.addInvoiceMaster(
                request, InvoiceMasterPydanticData, db
            )
            InvoiceMasterDictData["InvMasterID"] = AddInvoiceMasterResponse["InvMasterID"]
            InvoiceMasterDictDataList.append(InvoiceMasterDictData)
        pprint(InvoiceMasterDictDataList)

    return {"message": "success"}
