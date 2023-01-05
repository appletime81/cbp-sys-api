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
from utils.utils import convert_time_to_str, cal_fee_amount_post

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
    InvoiceWKMasterDictData = invoice_data["InvoiceWKMaster"]

    # IsLiable: True
    if InvoiceWKMasterDictData.get("IsLiability"):
        # 1. create InvoiceWKMaster
        InvoiceWKMasterDictData["CreateDate"] = convert_time_to_str(
            datetime.now()
        )  # add CreateDate
        InvoiceWKMasterPydanticData = InvoiceWKMasterSchema(**InvoiceWKMasterDictData)
        AddInvoiceWKMasterResponse = await service.addInvoiceWKMaster(
            request, InvoiceWKMasterPydanticData, db
        )
        WKMasterID = AddInvoiceWKMasterResponse["WKMasterID"]

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
        for i, InvoiceWKDetailDictData in enumerate(newInvoiceWKDetailDictDataList):
            InvoiceWKDetailPydanticData = InvoiceWKDetailSchema(
                **InvoiceWKDetailDictData
            )
            addInvoiceWKDetailResponse = await service.addInvoiceWKDetail(
                request, InvoiceWKDetailPydanticData, db
            )
            newInvoiceWKDetailDictDataList[i][
                "WKDetailID"
            ] = addInvoiceWKDetailResponse["WKDetailID"]

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
            addInvoiceMasterResponse = await service.addInvoiceMaster(
                request, InvoiceMasterPydanticData, db
            )
            InvoiceMasterDictData["InvMasterID"] = addInvoiceMasterResponse[
                "InvMasterID"
            ]
            InvoiceMasterDictDataList.append(InvoiceMasterDictData)

        # 4. create InvoiceDetail
        InvoiceDetailDictDataList = []
        for InvoiceWKDetailDictData in newInvoiceWKDetailDictDataList:
            for InvoiceMasterDictData in InvoiceMasterDictDataList:
                InvoiceDetailDictData = {}
                InvMasterID = InvoiceMasterDictData["InvMasterID"]
                PartyName = InvoiceMasterDictData["PartyName"]
                WKMasterID = InvoiceWKDetailDictData["WKMasterID"]
                WKDetailID = InvoiceWKDetailDictData["WKDetailID"]
                InvoiceNo = InvoiceWKDetailDictData["InvoiceNo"]
                SupplierID = InvoiceWKDetailDictData["SupplierID"]
                SubmarineCable = InvoiceWKDetailDictData["SubmarineCable"]
                BillMilestone = InvoiceWKDetailDictData["BillMilestone"]
                FeeItem = InvoiceWKDetailDictData["FeeItem"]
                FeeAmount = InvoiceWKDetailDictData["FeeAmount"]

                getLiabilityCondition = (
                    f"BillMilestone={BillMilestone}&PartyName={PartyName}"
                )
                LiabilityDatas = await service.getLiability(
                    request, getLiabilityCondition, db
                )

                InvoiceDetailDictData["InvMasterID"] = InvMasterID
                InvoiceDetailDictData["WKMasterID"] = WKMasterID
                InvoiceDetailDictData["WKDetailID"] = WKDetailID
                InvoiceDetailDictData["InvoiceNo"] = InvoiceNo
                InvoiceDetailDictData["PartyName"] = PartyName
                InvoiceDetailDictData["SupplierID"] = SupplierID
                InvoiceDetailDictData["SubmarineCable"] = SubmarineCable
                InvoiceDetailDictData["BillMilestone"] = BillMilestone
                InvoiceDetailDictData["FeeItem"] = FeeItem
                InvoiceDetailDictData["FeeAmountPre"] = FeeAmount
                InvoiceDetailDictData["LBRatio"] = LiabilityDatas.first().LBRatio
                InvoiceDetailDictData["FeeAmountPost"] = cal_fee_amount_post(
                    LiabilityDatas.first().LBRatio, FeeAmount
                )
                InvoiceDetailDictData["Difference"] = 0

                # dict to pydantic
                InvoiceDetailPydanticData = InvoiceDetailSchema(**InvoiceDetailDictData)
                addInvoiceDetailResponse = await service.addInvoiceDetail(
                    request, InvoiceDetailPydanticData, db
                )
                InvoiceDetailDictData["InvDetailID"] = addInvoiceDetailResponse[
                    "InvDetailID"
                ]
                InvoiceDetailDictDataList.append(InvoiceDetailDictData)
        pprint(InvoiceDetailDictDataList)

    if not InvoiceWKMasterDictData.get("IsLiability"):
        # 1. create InvoiceWKMaster
        InvoiceWKMasterDictData["CreateDate"] = convert_time_to_str(
            datetime.now()
        )  # add CreateDate
        InvoiceWKMasterPydanticData = InvoiceWKMasterSchema(**InvoiceWKMasterDictData)
        AddInvoiceWKMasterResponse = await service.addInvoiceWKMaster(
            request, InvoiceWKMasterPydanticData, db
        )
        WKMasterID = AddInvoiceWKMasterResponse["WKMasterID"]

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
        for i, InvoiceWKDetailDictData in enumerate(newInvoiceWKDetailDictDataList):
            InvoiceWKDetailPydanticData = InvoiceWKDetailSchema(
                **InvoiceWKDetailDictData
            )
            addInvoiceWKDetailResponse = await service.addInvoiceWKDetail(
                request, InvoiceWKDetailPydanticData, db
            )
            newInvoiceWKDetailDictDataList[i][
                "WKDetailID"
            ] = addInvoiceWKDetailResponse["WKDetailID"]

        # 3. create InvoiceMaster
        InvoiceMasterDictDataList = []
        InvoiceMasterDictData = {}
        InvoiceMasterDictData.update(
            {
                "WKMasterID": WKMasterID,
                "InvoiceNo": InvoiceWKMasterDictData["InvoiceNo"],
                "PartyName": InvoiceWKMasterDictData["PartyName"],
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
        addInvoiceMasterResponse = await service.addInvoiceMaster(
            request, InvoiceMasterPydanticData, db
        )
        InvoiceMasterDictData["InvMasterID"] = addInvoiceMasterResponse["InvMasterID"]
        InvoiceMasterDictDataList.append(InvoiceMasterDictData)

        # 4. create InvoiceDetail
        InvoiceDetailDictDataList = []
        for InvoiceWKDetailDictData in newInvoiceWKDetailDictDataList:
            InvoiceDetailDictData = {}
            InvMasterID = InvoiceMasterDictData["InvMasterID"]
            PartyName = InvoiceWKMasterDictData["PartyName"]
            WKMasterID = InvoiceWKDetailDictData["WKMasterID"]
            WKDetailID = InvoiceWKDetailDictData["WKDetailID"]
            InvoiceNo = InvoiceWKDetailDictData["InvoiceNo"]
            SupplierID = InvoiceWKDetailDictData["SupplierID"]
            SubmarineCable = InvoiceWKDetailDictData["SubmarineCable"]
            BillMilestone = InvoiceWKDetailDictData["BillMilestone"]
            FeeItem = InvoiceWKDetailDictData["FeeItem"]
            FeeAmount = InvoiceWKDetailDictData["FeeAmount"]

            InvoiceDetailDictData["InvMasterID"] = InvMasterID
            InvoiceDetailDictData["WKMasterID"] = WKMasterID
            InvoiceDetailDictData["WKDetailID"] = WKDetailID
            InvoiceDetailDictData["InvoiceNo"] = InvoiceNo
            InvoiceDetailDictData["PartyName"] = PartyName
            InvoiceDetailDictData["SupplierID"] = SupplierID
            InvoiceDetailDictData["SubmarineCable"] = SubmarineCable
            InvoiceDetailDictData["BillMilestone"] = BillMilestone
            InvoiceDetailDictData["FeeItem"] = FeeItem
            InvoiceDetailDictData["FeeAmountPre"] = FeeAmount
            InvoiceDetailDictData["LBRatio"] = 100
            InvoiceDetailDictData["FeeAmountPost"] = cal_fee_amount_post(
                InvoiceDetailDictData["LBRatio"], FeeAmount
            )
            InvoiceDetailDictData["Difference"] = 0

            # dict to pydantic
            InvoiceDetailPydanticData = InvoiceDetailSchema(**InvoiceDetailDictData)
            addInvoiceDetailResponse = await service.addInvoiceDetail(
                request, InvoiceDetailPydanticData, db
            )
            InvoiceDetailDictData["InvDetailID"] = addInvoiceDetailResponse[
                "InvDetailID"
            ]
            InvoiceDetailDictDataList.append(InvoiceDetailDictData)

    return {"message": "success"}
