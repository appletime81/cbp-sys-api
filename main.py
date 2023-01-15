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
@app.post(f"{ROOT_URL}/generateInvoiceWKMaster&InvoiceWKDetail")
async def generateInvoiceWKMasterInvoiceWKDetailInvoiceMasterInvoiceDetail(
    request: Request,
    db: Session = Depends(get_db),
):
    invoice_data = await request.json()
    # ---------- Step1. Generate InvoiceWKMaster ----------

    # get invoice wk master data
    InvoiceWKMasterDictData = invoice_data["InvoiceWKMaster"]

    # covert InvoiceWKMasterDictData to Pydantic model
    InvoiceWKMasterSchemaData = InvoiceWKMasterSchema(**InvoiceWKMasterDictData)

    # save InvoiceWKMaster to db
    crud = CRUD(db, InvoiceWKMasterDBModel)
    crud.create(InvoiceWKMasterSchemaData)

    justCreatedInvoiceWKMasterID = crud.get_with_condition(InvoiceWKMasterDictData)[
        0
    ].WKMasterID
    print("justCreatedInvoiceWKMasterID", justCreatedInvoiceWKMasterID)

    # ---------- Step2. Generate InvoiceWKDetail ----------

    # get invoice wk detail data
    InvoiceWKDetailDictDataList = invoice_data["InvoiceWKDetail"]

    for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
        # covert InvoiceWKDetailDictData to Pydantic model
        InvoiceWKDetailDictData["WKMasterID"] = justCreatedInvoiceWKMasterID
        InvoiceWKDetailDictData["InvoiceNo"] = InvoiceWKMasterDictData["InvoiceNo"]
        InvoiceWKDetailDictData["WorkTitle"] = InvoiceWKMasterDictData["WorkTitle"]
        InvoiceWKDetailDictData["SupplierName"] = InvoiceWKMasterDictData[
            "SupplierName"
        ]
        InvoiceWKDetailDictData["SubmarineCable"] = InvoiceWKMasterDictData[
            "SubmarineCable"
        ]
        InvoiceWKDetailSchemaData = InvoiceWKDetailSchema(**InvoiceWKDetailDictData)

        # save InvoiceWKDetail to db
        crud = CRUD(db, InvoiceWKDetailDBModel)
        crud.create(InvoiceWKDetailSchemaData)

    return {"message": "success"}


@app.get(ROOT_URL + "/getInvoiceMaster&InvoiceDetailStream/WKMasterID={WKMasterID}")
async def getInvoiceMasterInvoiceDetailStram(
    request: Request,
    WKMasterID: int,
    db: Session = Depends(get_db),
):
    # Step1. Get InvoiceWKMaster
    InvoiceWKMasterDataList = await service.getInvoiceWKMaster(
        request, f"WKMasterID={WKMasterID}", db
    )
    # print(InvoiceWKMasterDataList)
    InvoiceWKMasterData = InvoiceWKMasterDataList[0]
    InvoiceWKMasterDictData = orm_to_pydantic(
        InvoiceWKMasterData, InvoiceWKMasterSchema
    ).dict()
    WorkTitle = InvoiceWKMasterDictData["WorkTitle"]
    SubmarineCable = InvoiceWKMasterDictData["SubmarineCable"]
    # pprint(InvoiceWKMasterDictData)

    # Step2. Get InvoiceWKDetail
    InvoiceWKDetailDataList = await service.getInvoiceWKDetail(
        request, f"WKMasterID={WKMasterID}", db
    )
    InvoiceWKDetailDictDataList = [
        orm_to_pydantic(InvoiceWKDetailData, InvoiceWKDetailSchema).dict()
        for InvoiceWKDetailData in InvoiceWKDetailDataList
    ]

    if InvoiceWKMasterDictData.get("IsLiability"):
        # Step3. Generate InvoiceMaster
        # get all Liability
        newLiabilityDataList = []
        for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
            LiabilityDataList = await service.getLiability(
                request,
                f"SubmarineCable={SubmarineCable}&WorkTitle={WorkTitle}&BillMilestone={InvoiceWKDetailDictData.get('BillMilestone')}",
                db,
            )
            newLiabilityDataList.append(LiabilityDataList)
        LiabilityDictDataList = [
            orm_to_pydantic(LiabilityData, LiabilitySchema).dict()
            for LiabilityDataList in newLiabilityDataList
            for LiabilityData in LiabilityDataList
        ]
        # print("-" * 50)
        # pprint(LiabilityDictDataList)
        LiabilityDataFrameDataList = [
            pd.DataFrame(dict([(k, [v]) for k, v in LiabilityDictData.items()]))
            for LiabilityDictData in LiabilityDictDataList
        ]
        LiabilityDataFrameData = dflist_to_df(LiabilityDataFrameDataList)
        # print("-" * 50)
        # print(LiabilityDataFrameData)

        # get all PartyName
        PartyNameList = list(
            set([LiabilityData.PartyName for LiabilityData in LiabilityDataList])
        )

        InvoiceMasterDictDataList = []
        for PartyName in PartyNameList:
            InvoiceMasterDictData = {
                "WKMasterID": WKMasterID,
                "InvoiceNo": InvoiceWKMasterDictData["InvoiceNo"],
                "PartyName": PartyName,
                "SubmarineCable": SubmarineCable,
                "WorkTitle": WorkTitle,
                "IssueDate": InvoiceWKMasterDictData["IssueDate"],
                "DueDate": InvoiceWKMasterDictData["DueDate"],
                "IsPro": InvoiceWKMasterDictData["IsPro"],
                "SupplierName": InvoiceWKMasterDictData["SupplierName"],
                "ContractType": InvoiceWKMasterDictData["ContractType"],
            }
            InvoiceMasterDictDataList.append(InvoiceMasterDictData)
        crud = CRUD(db, InvoiceWKMasterDBModel)
        InvMasterID = (
            crud.get_max_id(InvoiceMasterDBModel.InvMasterID) + 1
            if crud.get_max_id(InvoiceMasterDBModel.InvMasterID)
            else 1
        )
        print(f"{'-' * 50} InvMasterID {'-' * 50}")
        print(InvMasterID)

        # Step4. Generate InvoiceDetail
        InvoiceDetailDictDataList = []
        for InvoiceMasterDictData in InvoiceMasterDictDataList:
            for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
                LBRatio = LiabilityDataFrameData[
                    (
                        LiabilityDataFrameData["PartyName"]
                        == InvoiceMasterDictData["PartyName"]
                    )
                    & (
                        LiabilityDataFrameData["BillMilestone"]
                        == InvoiceWKDetailDictData["BillMilestone"]
                    )
                    & (
                        LiabilityDataFrameData["WorkTitle"]
                        == InvoiceMasterDictData["WorkTitle"]
                    )
                ]["LBRatio"].values[0]

                InvoiceDetailDictData = {
                    "WKMasterID": WKMasterID,
                    "WKDetailID": InvoiceWKDetailDictData["WKDetailID"],
                    "InvMasterID": InvMasterID,
                    "InvoiceNo": InvoiceWKMasterDictData["InvoiceNo"],
                    "PartyName": InvoiceMasterDictData["PartyName"],
                    "SupplierName": InvoiceMasterDictData["SupplierName"],
                    "SubmarineCable": InvoiceMasterDictData["SubmarineCable"],
                    "WorkTitle": InvoiceMasterDictData["WorkTitle"],
                    "BillMilestone": InvoiceWKDetailDictData["BillMilestone"],
                    "FeeItem": InvoiceWKDetailDictData["FeeItem"],
                    "LBRatio": LBRatio,
                    "FeeAmountPre": InvoiceWKDetailDictData["FeeAmount"],
                    "FeeAmountPost": cal_fee_amount_post(
                        LBRatio, InvoiceWKDetailDictData["FeeAmount"]
                    ),
                    "Difference": 0,
                }
                InvoiceDetailDictDataList.append(InvoiceDetailDictData)
    else:
        pass
    print(len(InvoiceDetailDictDataList))
    return InvoiceDetailDictDataList


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
