import os
import io
import json
import uuid
import copy
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

pd.set_option("display.max_columns", None)

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
                    "SupplierName": InvoiceWKMasterDictData["SupplierName"],
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


@app.get(ROOT_URL + "/searchInvoiceWKMaster/{urlCondition}")
async def searchInvoiceWKMaster(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    dict_condition = convert_url_condition_to_dict_ignore_date(urlCondition)
    dict_condition_copy = deepcopy(dict_condition)

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
    print("-" * 50)
    print(WKMasterIDList)
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
        print("-" * 50)
        print(tempDictCondition)
        dict_condition_list.append(tempDictCondition)

    # get InvoiceWKMaster datas
    InvoiceWKMasterDataList = []
    for dict_condition in dict_condition_list:
        url_condition_for_invoice_wk_master = convert_dict_condition_to_url(
            deepcopy(dict_condition)
        )
        print(url_condition_for_invoice_wk_master)
        InvoiceWKMasterData = await service.getInvoiceWKMaster(
            request, url_condition_for_invoice_wk_master, db
        )
        InvoiceWKMasterDataList.append(InvoiceWKMasterData)

    pprint(InvoiceWKMasterDataList)

    # get all InvoiceDetail
    return InvoiceWKMasterDataList


# -------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------ BillMaster and  BillDetail ------------------------------
@app.post(
    f"{ROOT_URL}/generateBillMaster&BillDetail",
)
async def generateBillMasterAndBillDetail(
    request: Request,
    invoice_data: dict = Body(...),
    db: Session = Depends(get_db),
):
    # get condition
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
