import os
import io
import json
import uuid
import copy

from fastapi.middleware.cors import CORSMiddleware

import service
import pandas as pd

from crud import *
from pprint import pprint
from get_db import get_db
from copy import deepcopy
from datetime import datetime
from fastapi import FastAPI, Depends, Request, Body
from utils.utils import (
    dflist_to_df,
    convert_time_to_str,
    cal_fee_amount_post,
    convert_dict_condition_to_url,
    convert_url_condition_to_dict_ignore_date,
)
from utils.orm_pydantic_convert import orm_to_pydantic

pd.set_option("display.max_columns", None)

app = FastAPI()

ROOT_URL = "/api/v1"

app.include_router(service.router, prefix=ROOT_URL, tags=["service"])

# allow middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------ InvoiceWKMaster and InvoiceWKDetail and InvoiceMaster and InvoiceDetail ------------------------------
@app.post(
    f"{ROOT_URL}/generateInvoiceWKMaster&InvoiceWKDetail&InvoiceMaster&InvoiceDetail"
)
async def generateInvoiceWKMasterInvoiceWKDetailInvoiceMasterInvoiceDetail(
    request: Request,
    db: Session = Depends(get_db),
):

    invoice_data = await request.json()
    InvoiceWKMasterDictData = invoice_data["InvoiceWKMaster"]
    print("-" * 25 + " invoice_data " + "-" * 25)
    pprint(invoice_data)
    # 1. create InvoiceWKMaster
    InvoiceWKMasterDictData["CreateDate"] = convert_time_to_str(
        datetime.now()
    )  # add CreateDate
    InvoiceWKMasterPydanticData = InvoiceWKMasterSchema(**InvoiceWKMasterDictData)
    AddInvoiceWKMasterResponse = await service.addInvoiceWKMaster(
        request, InvoiceWKMasterPydanticData, db
    )
    WKMasterID = AddInvoiceWKMasterResponse["WKMasterID"]

    # 2. prepare for creating InvoiceWKDetail (declare variable)
    InvoiceWKDetailDictDataList = invoice_data["InvoiceWKDetail"]
    newInvoiceWKDetailDictDataList = []

    # IsLiable: True
    if InvoiceWKMasterDictData.get("IsLiability"):
        # 2. create InvoiceWKDetail
        for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
            InvoiceWKDetailDictData.update(
                {
                    "WKMasterID": WKMasterID,
                    "InvoiceNo": InvoiceWKMasterDictData["InvoiceNo"],
                    "SupplierName": InvoiceWKMasterDictData["SupplierName"],
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
        InvoiceMasterDictDataList = []
        getLiabilityUrlConditionList = []
        for InvoiceWKDetailDictData in newInvoiceWKDetailDictDataList:
            getLiabilityUrlConditionList.append(
                f"BillMilestone={InvoiceWKDetailDictData['BillMilestone']}&SubmarineCable={InvoiceWKMasterDictData['SubmarineCable']}"
            )
        getLiabilityUrlConditionList = list(set(getLiabilityUrlConditionList))

        # 3.2 get all PartyName, not duplicate
        PartyNameList = []
        for getLiabilityUrlCondition in getLiabilityUrlConditionList:
            LiabilityDatas = await service.getLiability(
                request, getLiabilityUrlCondition, db
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
                    "SupplierName": InvoiceWKMasterDictData["SupplierName"],
                    "ContractType": InvoiceWKMasterDictData["ContractType"],
                    "IssueDate": InvoiceWKMasterDictData["IssueDate"],
                    "DueDate": InvoiceWKMasterDictData["DueDate"],
                    "SubmarineCable": InvoiceWKMasterDictData["SubmarineCable"],
                    "Status": InvoiceWKMasterDictData["Status"],
                    "IsPro": 0 if not InvoiceWKMasterDictData["IsPro"] else 1,
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
                SupplierName = InvoiceWKDetailDictData["SupplierName"]
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
                InvoiceDetailDictData["SupplierName"] = SupplierName
                InvoiceDetailDictData["SubmarineCable"] = SubmarineCable
                InvoiceDetailDictData["BillMilestone"] = BillMilestone
                InvoiceDetailDictData["FeeItem"] = FeeItem
                InvoiceDetailDictData["FeeAmountPre"] = FeeAmount
                InvoiceDetailDictData["LBRatio"] = LiabilityDatas.first().LBRatio
                InvoiceDetailDictData["FeeAmountPost"] = cal_fee_amount_post(
                    LiabilityDatas.first().LBRatio, float(FeeAmount)
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
        # pprint(InvoiceDetailDictDataList)

    if not InvoiceWKMasterDictData.get("IsLiability"):
        # 2. create InvoiceWKDetail
        for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
            InvoiceWKDetailDictData.update(
                {
                    "WKMasterID": WKMasterID,
                    "InvoiceNo": InvoiceWKMasterDictData["InvoiceNo"],
                    "SupplierName": InvoiceWKMasterDictData["SupplierName"],
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
                "SupplierName": InvoiceWKMasterDictData["SupplierName"],
                "ContractType": InvoiceWKMasterDictData["ContractType"],
                "IssueDate": InvoiceWKMasterDictData["IssueDate"],
                "DueDate": InvoiceWKMasterDictData["DueDate"],
                "SubmarineCable": InvoiceWKMasterDictData["SubmarineCable"],
                "Status": InvoiceWKMasterDictData["Status"],
                "IsPro": 0 if not InvoiceWKMasterDictData["IsPro"] else 1,
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
            SupplierName = InvoiceWKDetailDictData["SupplierName"]
            SubmarineCable = InvoiceWKDetailDictData["SubmarineCable"]
            BillMilestone = InvoiceWKDetailDictData["BillMilestone"]
            FeeItem = InvoiceWKDetailDictData["FeeItem"]
            FeeAmount = InvoiceWKDetailDictData["FeeAmount"]

            InvoiceDetailDictData["InvMasterID"] = InvMasterID
            InvoiceDetailDictData["WKMasterID"] = WKMasterID
            InvoiceDetailDictData["WKDetailID"] = WKDetailID
            InvoiceDetailDictData["InvoiceNo"] = InvoiceNo
            InvoiceDetailDictData["PartyName"] = PartyName
            InvoiceDetailDictData["SupplierName"] = SupplierName
            InvoiceDetailDictData["SubmarineCable"] = SubmarineCable
            InvoiceDetailDictData["BillMilestone"] = BillMilestone
            InvoiceDetailDictData["FeeItem"] = FeeItem
            InvoiceDetailDictData["FeeAmountPre"] = FeeAmount
            InvoiceDetailDictData["LBRatio"] = 100
            InvoiceDetailDictData["FeeAmountPost"] = cal_fee_amount_post(
                InvoiceDetailDictData["LBRatio"], float(FeeAmount)
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


@app.get(ROOT_URL + "/searchInvoiceWKMaster/{urlCondition}")
async def searchInvoiceWKMaster(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    if urlCondition == "all":
        # get all InvoiceWKMaster datas
        InvoiceWKMasterList = await service.getInvoiceWKMaster(request, "all", db)
        InvoiceWKMasterDictList = []
        for item in InvoiceWKMasterList:
            item_dict = orm_to_pydantic(item, InvoiceWKMasterSchema).dict()
            InvoiceWKMasterDictList.append(item_dict)

        # generate result with InvoiceWKMaster datas and InvoiceWKDetail datas
        resultDataList = []
        for InvoiceWKMasterDictData in InvoiceWKMasterDictList:
            InvoiceWKDetailDatas = await service.getInvoiceWKDetail(
                request, f"WKMasterID={InvoiceWKMasterDictData['WKMasterID']}", db
            )
            InvoiceWKDetailDictDatas = [
                orm_to_pydantic(item, InvoiceWKDetailSchema).dict()
                for item in InvoiceWKDetailDatas
            ]
            resultDataList.append(
                {
                    "InvoiceWKMaster": InvoiceWKMasterDictData,
                    "InvoiceWKDetail": InvoiceWKDetailDictDatas,
                }
            )
    else:
        dict_condition = convert_url_condition_to_dict_ignore_date(urlCondition)
        dict_condition_copy = deepcopy(dict_condition)
        # pprint(dict_condition)

        # remove Date's condition in dict_condition_copy
        containDateStringList = [k for k in dict_condition_copy if "Date" in k]
        for k in containDateStringList:
            dict_condition_copy.pop(k)

        # remove Status's condition in dict_condition_copy
        if "Status" in dict_condition_copy:
            dict_condition_copy.pop("Status")

        # convert dict_condition_copy condition to url condition
        url_condition_for_invoice_detail_master = convert_dict_condition_to_url(
            dict_condition_copy
        )

        # get InvoiceDetail datas
        InvoiceDetailDataList = await service.getInvoiceDetail(
            request, url_condition_for_invoice_detail_master, db
        )

        # get all InvoiceDetail's WKMasterID
        WKMasterIDList = [
            InvoiceDetailData.WKMasterID for InvoiceDetailData in InvoiceDetailDataList
        ]
        WKMasterIDList = list(set(WKMasterIDList))

        # remove PartyName, BillMilestone in dict_condition
        if "PartyName" in dict_condition:
            dict_condition.pop("PartyName")
        if "BillMilestone" in dict_condition:
            dict_condition.pop("BillMilestone")

        # generate dict condition list for get InvoiceWKMaster
        dict_condition_list = []
        for WKMasterID in WKMasterIDList:
            tempDictCondition = deepcopy(dict_condition)
            tempDictCondition["WKMasterID"] = WKMasterID
            dict_condition_list.append(tempDictCondition)

        # get InvoiceWKMaster datas
        InvoiceWKMasterDataList = []
        for dict_condition in dict_condition_list:
            url_condition_for_invoice_wk_master = convert_dict_condition_to_url(
                deepcopy(dict_condition)
            )
            InvoiceWKMasterData = await service.getInvoiceWKMaster(
                request, url_condition_for_invoice_wk_master, db
            )
            InvoiceWKMasterDataList.append(InvoiceWKMasterData)

        newInvoiceWKMasterDataList = []
        for InvoiceWKMasterData in InvoiceWKMasterDataList:
            if type(InvoiceWKMasterData) == list:
                newInvoiceWKMasterDataList += InvoiceWKMasterData
            else:
                newInvoiceWKMasterDataList.append(InvoiceWKMasterData)
        InvoiceWKMasterDataList = deepcopy(newInvoiceWKMasterDataList)
        InvoiceWKMasterDictDataList = [
            orm_to_pydantic(InvoiceWKMasterData, InvoiceWKMasterSchema).dict()
            for InvoiceWKMasterData in InvoiceWKMasterDataList
        ]
        # pprint(InvoiceWKMasterDictDataList)

        # get all InvoiceWKDetail datas
        InvoiceWKDetailDatasList = []
        for WKMasterID in WKMasterIDList:
            url_condition_for_invoice_wk_detail = f"WKMasterID={WKMasterID}"
            InvoiceWKDetailDatas = await service.getInvoiceWKDetail(
                request, url_condition_for_invoice_wk_detail, db
            )
            InvoiceWKDetailDatasList.append(InvoiceWKDetailDatas)

        newInvoiceWKDetailDatasList = []
        for InvoiceWKDetailDatas in InvoiceWKDetailDatasList:
            if type(InvoiceWKDetailDatas) == list:
                newInvoiceWKDetailDatasList += InvoiceWKDetailDatas
            else:
                newInvoiceWKDetailDatasList.append(InvoiceWKDetailDatas)
        InvoiceWKDetailDatasList = deepcopy(newInvoiceWKDetailDatasList)
        InvoiceWKDetailDictDatasList = [
            orm_to_pydantic(InvoiceWKDetailData, InvoiceWKDetailSchema).dict()
            for InvoiceWKDetailData in InvoiceWKDetailDatasList
        ]
        # pprint(InvoiceWKDetailDictDatasList)

        resultDataList = []
        for InvoiceWKMasterDictData in InvoiceWKMasterDictDataList:
            tempDict = {"InvoiceWKMaster": deepcopy(InvoiceWKMasterDictData)}
            tempDict["InvoiceWKDetail"] = []
            for InvoiceWKDetailDictData in InvoiceWKDetailDictDatasList:
                if (
                    InvoiceWKDetailDictData["WKMasterID"]
                    == InvoiceWKMasterDictData["WKMasterID"]
                ):
                    tempDict["InvoiceWKDetail"].append(InvoiceWKDetailDictData)
            resultDataList.append(tempDict)

    return resultDataList


# -------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------ BillMaster and  BillDetail ------------------------------
@app.post(
    f"{ROOT_URL}/generateBillMaster&BillDetail",
)
async def generateBillMasterAndBillDetail(
    request: Request,
    db: Session = Depends(get_db),
):
    # get condition
    invoice_data = await request.json()
    WKMasterID = invoice_data["WKMasterID"]
    DueDate = invoice_data["DueDate"]
    if not WKMasterID or not DueDate:  # check condition
        return {"message": "please input WKMasterID and DueDate"}
    dict_condition = {"WKMasterID": WKMasterID}
    url_condition = convert_dict_condition_to_url(dict_condition)

    # get IsPro status from InvoiceWKMaster
    InvoiceWKMasterData = await service.getInvoiceWKMaster(request, url_condition, db)
    if not InvoiceWKMasterData:  # check InvoiceWKMasterData if exist
        return {"message": "no InvoiceWKMasterData"}
    IsPRo = InvoiceWKMasterData.IsPro
    SubmarineCable = InvoiceWKMasterData.SubmarineCable

    # get all InvoiceDetail by "InvoiceWKMasterID"
    InvoiceDetailDataList = await service.getInvoiceDetail(request, url_condition, db)

    # convert InvoiceDetailDataList to dataframe format
    dfInvoiceDetailDataList = [
        pd.DataFrame(InvoiceDetailData.__dict__, index=[0])
        for InvoiceDetailData in InvoiceDetailDataList
    ]
    dfInvoiceDetailData = dflist_to_df(dfInvoiceDetailDataList)

    # let dfInvoiceDetailData group by PartyName
    dfInvoiceDetailDataGroupByPartyName = (
        dfInvoiceDetailData.groupby(["PartyName"])["BillMilestone"]
        .apply(list)
        .reset_index(name="BillMilestoneList")
    )
    dfInvoiceDetailDataGroupByPartyName.to_csv(
        "dfInvoiceDetailDataGroupByPartyName.csv"
    )

    # generate BillMaster
    BillMasterDictDataList = []
    for index, row in dfInvoiceDetailDataGroupByPartyName.iterrows():
        BillMasterDictData = {}
        subBillingNoString = ""
        for BillMilestone in list(set(row["BillMilestoneList"])):
            subBillingNoString += f"{BillMilestone}-"

        BillingNo = f'{SubmarineCable}-CBP-{row["PartyName"]}-{subBillingNoString[:-1]}'
        PartyName = row["PartyName"]
        CreateDate = convert_time_to_str(datetime.now())
        Status = "Initial"
        BillMasterDictData.update(
            {
                "BillingNo": BillingNo,
                "PartyName": PartyName,
                "CreateDate": CreateDate,
                "DueDate": DueDate,
                "Status": Status,
                "IsPro": IsPRo,
            }
        )
        BillMasterPydanticData = BillMasterSchema(**BillMasterDictData)
        addBillMasterResponse = await service.addBillMaster(
            request, BillMasterPydanticData, db
        )
        BillMasterDictData["BillMasterID"] = addBillMasterResponse["BillMasterID"]
        BillMasterDictDataList.append(BillMasterDictData)
    pprint(BillMasterDictDataList)

    return {"message": "success"}


# ----------------------------------------------------------------------------------------
