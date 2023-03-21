from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

import service.InvoiceWKMaster.app as InvoiceWKMasterApp
import service.InvoiceWKDetail.app as InvoiceWKDetailApp
import service.InvoiceMaster.app as InvoiceMasterApp
import service.InvoiceDetail.app as InvoiceDetailApp
import service.Liability.app as LiabilityApp
import service.Parties.app as PartiesApp
import service.SubmarineCables.app as SubmarineCablesApp
import service.Suppliers.app as SuppliersApp
import service.Letter.app as LetterApp

from crud import *
from get_db import get_db
from service.InvoiceDetail.app import router as InvoiceDetailRouter
from service.InvoiceMaster.app import router as InvoiceMasterRouter
from service.InvoiceWKDetail.app import router as InvoiceWKDetailRouter
from service.InvoiceWKMaster.app import router as InvoiceWKMasterRouter
from service.Liability.app import router as LiabilityRouter
from service.Parties.app import router as PartiesRouter
from service.SubmarineCables.app import router as SubmarineCablesRouter
from service.Suppliers.app import router as SuppliersRouter
from service.BillMilestone.app import router as BillMilestoneRouter
from service.CreditBalance.app import router as CreditBalanceRouter
from service.Letter.app import router as LetterRouter
from service.BillMaster.app import router as BillMasterRouter
from service.Corporates.app import router as CorporatesRouter
from service.Contracts.app import router as ContractsRouter
from service.SubmarineCables.app import router as SubmarineCablesRouter
from service.PartiesByContract.app import router as PartiesByContractRouter
from service.SuppliersByContract.app import router as SuppliersByContractRouter
from service.UploadFile.app import router as UploadFileRouter
from service.Users.app import router as UsersRouter
from utils.utils import *
from utils.orm_pydantic_convert import *

pd.set_option("display.max_columns", None)

app = FastAPI()

ROOT_URL = "/api/v1"


app.include_router(InvoiceWKMasterRouter, prefix=ROOT_URL, tags=["InvoiceWKMaster"])
app.include_router(InvoiceWKDetailRouter, prefix=ROOT_URL, tags=["InvoiceWKDetail"])
app.include_router(InvoiceMasterRouter, prefix=ROOT_URL, tags=["InvoiceMaster"])
app.include_router(InvoiceDetailRouter, prefix=ROOT_URL, tags=["InvoiceDetail"])
app.include_router(LiabilityRouter, prefix=ROOT_URL, tags=["Liability"])
app.include_router(PartiesRouter, prefix=ROOT_URL, tags=["Parties"])
app.include_router(SubmarineCablesRouter, prefix=ROOT_URL, tags=["SubmarineCables"])
app.include_router(SuppliersRouter, prefix=ROOT_URL, tags=["Suppliers"])
app.include_router(BillMilestoneRouter, prefix=ROOT_URL, tags=["BillMilestone"])
app.include_router(CreditBalanceRouter, prefix=ROOT_URL, tags=["CreditBalance"])
app.include_router(LetterRouter, prefix=ROOT_URL, tags=["Letter"])
app.include_router(BillMasterRouter, prefix=ROOT_URL, tags=["BillMaster"])
app.include_router(CorporatesRouter, prefix=ROOT_URL, tags=["Corporates"])
app.include_router(ContractsRouter, prefix=ROOT_URL, tags=["Contracts"])
app.include_router(SubmarineCablesRouter, prefix=ROOT_URL, tags=["SubmarineCables"])
app.include_router(PartiesByContractRouter, prefix=ROOT_URL, tags=["PartiesByContract"])
app.include_router(
    SuppliersByContractRouter, prefix=ROOT_URL, tags=["SuppliersByContract"]
)
app.include_router(UploadFileRouter, prefix=ROOT_URL, tags=["ReceiveFile"])
app.include_router(UsersRouter, prefix=ROOT_URL, tags=["Users"])

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
    CreateDate = convert_time_to_str(datetime.now())
    # ---------- Step1. Generate InvoiceWKMaster ----------

    # get invoice wk master data
    InvoiceWKMasterDictData = invoice_data["InvoiceWKMaster"]

    # set CreateDate
    InvoiceWKMasterDictData["CreateDate"] = CreateDate

    # covert InvoiceWKMasterDictData to Pydantic model
    InvoiceWKMasterSchemaData = InvoiceWKMasterSchema(**InvoiceWKMasterDictData)

    # save InvoiceWKMaster to db
    crud = CRUD(db, InvoiceWKMasterDBModel)
    addResponse = crud.create(InvoiceWKMasterSchemaData)
    print("-" * 25 + " addResponse " + "-" * 25)
    print(addResponse.WKMasterID)
    print("-" * 25 + " addResponse " + "-" * 25)

    justCreatedInvoiceWKMasterID = addResponse.WKMasterID
    print("justCreatedInvoiceWKMasterID", addResponse.WKMasterID)

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


@app.get(ROOT_URL + "/getInvoiceWKMaster&InvoiceWKDetail/{urlCondition}")
async def searchInvoiceWKMaster(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    getResult = []

    # init CRUD
    crudInvoiceWKMaster = CRUD(db, InvoiceWKMasterDBModel)
    crudInvoiceWKDetail = CRUD(db, InvoiceWKDetailDBModel)

    # get query condition
    if urlCondition == "all":
        InvoiceWKMasterDataList = crudInvoiceWKMaster.get_all()
        InvoiceWKDetailDataList = crudInvoiceWKDetail.get_all()
        for InvoiceWKMasterData in InvoiceWKMasterDataList:
            getResult.append(
                {
                    "InvoiceWKMaster": InvoiceWKMasterData,
                    "InvoiceWKDetail": list(
                        filter(
                            lambda x: x.WKMasterID == InvoiceWKMasterData.WKMasterID,
                            InvoiceWKDetailDataList,
                        )
                    ),
                }
            )
        return getResult
    else:
        dictCondition = convert_url_condition_to_dict(urlCondition)

    date_condition = dict(filter(lambda x: "Date" in x[0], dictCondition.items()))
    status_condition = dict(filter(lambda x: "Status" in x[0], dictCondition.items()))
    newDictCondition = dict(
        filter(
            lambda x: "Date" not in x[0] and "Status" not in x[0], dictCondition.items()
        )
    )

    # -------------------------- get data from db --------------------------
    # get InvoiceWKDetail data from db
    InvoiceWKDetailDataList = crudInvoiceWKDetail.get_with_condition(newDictCondition)
    WKMasterIDList = [
        InvoiceWKDetailData.WKMasterID
        for InvoiceWKDetailData in InvoiceWKDetailDataList
    ]
    WKMasterIDList = list(set(WKMasterIDList))

    # get InvoiceWKMaster data from db
    InvoiceWKMasterDataList = crudInvoiceWKMaster.get_value_if_in_a_list(
        InvoiceWKMasterDBModel.WKMasterID, WKMasterIDList
    )

    if status_condition:
        if isinstance(status_condition["Status"], str):
            InvoiceWKMasterDataList = [
                InvoiceWKMasterData
                for InvoiceWKMasterData in InvoiceWKMasterDataList
                if InvoiceWKMasterData.Status == status_condition["Status"]
            ]
        else:
            InvoiceWKMasterDataList = [
                InvoiceWKMasterData
                for InvoiceWKMasterData in InvoiceWKMasterDataList
                if InvoiceWKMasterData.Status in status_condition["Status"]
            ]

    if date_condition:
        key = list(date_condition.keys())[0]
        col_name = key.replace("range", "")
        if date_condition[key]["gte"] == date_condition[key]["lte"]:
            date_condition[key]["gte"] = date_condition[key]["gte"][:10] + " 23:59:59"
        InvoiceWKMasterDataList = [
            InvoiceWKMasterData
            for InvoiceWKMasterData in InvoiceWKMasterDataList
            if str_time_convert_to_int(date_condition[key]["gte"])
            <= str_time_convert_to_int(orm_to_dict(InvoiceWKMasterData)[col_name])
            <= str_time_convert_to_int(date_condition[key]["lte"])
        ]

    # generate result
    for InvoiceWKMasterData in InvoiceWKMasterDataList:
        tempInvoiceWKDetailDataList = list(
            filter(
                lambda x: x.WKMasterID == InvoiceWKMasterData.WKMasterID,
                InvoiceWKDetailDataList,
            )
        )
        getResult.append(
            {
                "InvoiceWKMaster": InvoiceWKMasterData,
                "InvoiceWKDetail": tempInvoiceWKDetailDataList,
            }
        )

    return getResult


@app.get(ROOT_URL + "/getInvoiceMaster&InvoiceDetailStream/WKMasterID={WKMasterID}")
async def getInvoiceMasterInvoiceDetailStream(
    request: Request,
    WKMasterID: int,
    db: Session = Depends(get_db),
):
    # Step1. Get InvoiceWKMaster
    InvoiceWKMasterDataList = await InvoiceWKMasterApp.getInvoiceWKMaster(
        request, f"WKMasterID={WKMasterID}", db
    )

    InvoiceWKMasterData = InvoiceWKMasterDataList[0]
    InvoiceWKMasterDictData = orm_to_pydantic(
        InvoiceWKMasterData, InvoiceWKMasterSchema
    ).dict()
    TotalAmount = InvoiceWKMasterDictData.get("TotalAmount")
    WorkTitle = InvoiceWKMasterDictData["WorkTitle"]
    SubmarineCable = InvoiceWKMasterDictData["SubmarineCable"]

    # Step2. Get InvoiceWKDetail
    InvoiceWKDetailDataList = await InvoiceWKDetailApp.getInvoiceWKDetail(
        request, f"WKMasterID={WKMasterID}", db
    )
    InvoiceWKDetailDictDataList = [
        orm_to_pydantic(InvoiceWKDetailData, InvoiceWKDetailSchema).dict()
        for InvoiceWKDetailData in InvoiceWKDetailDataList
    ]

    # get max InvoiceMaster ID and generate InvoiceMasterID
    crud = CRUD(db, InvoiceMasterDBModel)
    InvMasterID = (
        crud.get_max_id(InvoiceMasterDBModel.InvMasterID) + 1
        if crud.get_max_id(InvoiceMasterDBModel.InvMasterID)
        else 1
    )

    if InvoiceWKMasterDictData.get("IsLiability"):
        # Step3. Generate InvoiceMaster
        # get all Liability
        newLiabilityDataList = []
        for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
            LiabilityDataList = await LiabilityApp.getLiability(
                request,
                f"SubmarineCable={SubmarineCable}&WorkTitle={WorkTitle}&BillMilestone={InvoiceWKDetailDictData.get('BillMilestone')}&End=false",
                db,
            )
            newLiabilityDataList.append(LiabilityDataList)
        LiabilityDictDataList = [
            orm_to_pydantic(LiabilityData, LiabilitySchema).dict()
            for LiabilityDataList in newLiabilityDataList
            for LiabilityData in LiabilityDataList
        ]

        if not LiabilityDictDataList:
            return {"message": "No Liability Data"}

        LiabilityDataFrameDataList = [
            pd.DataFrame(dict([(k, [v]) for k, v in LiabilityDictData.items()]))
            for LiabilityDictData in LiabilityDictDataList
        ]
        LiabilityDataFrameData = dflist_to_df(LiabilityDataFrameDataList)
        LiabilityDataFrameData = (
            LiabilityDataFrameData.drop_duplicates()
        )  # remove duplicates
        LiabilityDataFrameData.to_csv("LiabilityDataFrameData.csv", index=False)
        # get all PartyName
        PartyNameList = list(
            set([LiabilityData.PartyName for LiabilityData in LiabilityDataList])
        )

        InvoiceMasterDictDataList = []
        for i, PartyName in enumerate(PartyNameList):
            InvoiceMasterDictData = {
                "InvMasterID": InvMasterID + i,
                "WKMasterID": WKMasterID,
                "InvoiceNo": InvoiceWKMasterDictData["InvoiceNo"],
                "PartyName": PartyName,
                "SupplierName": InvoiceWKMasterDictData["SupplierName"],
                "SubmarineCable": SubmarineCable,
                "WorkTitle": WorkTitle,
                "IssueDate": convert_time_to_str(InvoiceWKMasterDictData["IssueDate"]),
                "DueDate": convert_time_to_str(InvoiceWKMasterDictData["DueDate"]),
                "IsPro": InvoiceWKMasterDictData["IsPro"],
                "ContractType": InvoiceWKMasterDictData["ContractType"],
                "Status": "",
            }
            InvoiceMasterDictDataList.append(InvoiceMasterDictData)

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
                    "InvMasterID": InvoiceMasterDictData["InvMasterID"],
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
        # Step1. generate InvoiceMaster
        InvoiceNo = InvoiceWKMasterDictData["InvoiceNo"]
        SupplierName = InvoiceWKMasterDictData["SupplierName"]
        ContractType = InvoiceWKMasterDictData["ContractType"]
        IssueDate = convert_time_to_str(InvoiceWKMasterDictData["IssueDate"])
        DueDate = convert_time_to_str(InvoiceWKMasterDictData["DueDate"])
        PartyName = InvoiceWKMasterDictData["PartyName"]
        IsPro = InvoiceWKMasterDictData["IsPro"]
        InvoiceMasterDictDataList = [
            {
                "InvMasterID": InvMasterID,
                "WKMasterID": WKMasterID,
                "InvoiceNo": InvoiceNo,
                "PartyName": PartyName,
                "SupplierName": SupplierName,
                "SubmarineCable": SubmarineCable,
                "WorkTitle": WorkTitle,
                "ContractType": ContractType,
                "IssueDate": IssueDate,
                "DueDate": DueDate,
                "Status": "",
                "IsPro": IsPro,
            }
        ]

        # Step2. generate InvoiceDetail
        InvoiceDetailDictDataList = []
        for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
            InvoiceDetailDictData = {
                "InvMasterID": InvMasterID,
                "WKMasterID": WKMasterID,
                "WKDetailID": InvoiceWKDetailDictData["WKDetailID"],
                "InvoiceNo": InvoiceNo,
                "PartyName": PartyName,
                "SupplierName": SupplierName,
                "SubmarineCable": SubmarineCable,
                "WorkTitle": WorkTitle,
                "BillMilestone": InvoiceWKDetailDictData["BillMilestone"],
                "FeeItem": InvoiceWKDetailDictData["FeeItem"],
                "LBRatio": 1,
                "FeeAmountPre": InvoiceWKDetailDictData["FeeAmount"],
                "FeeAmountPost": InvoiceWKDetailDictData["FeeAmount"],
                "Difference": 0,
            }
            InvoiceDetailDictDataList.append(InvoiceDetailDictData)

    streamResponse = {
        "TotalAmount": TotalAmount,
        "InvoiceMaster": InvoiceMasterDictDataList,
        "InvoiceDetail": InvoiceDetailDictDataList,
    }
    return streamResponse


@app.post(ROOT_URL + "/addInvoiceMaster&InvoiceDetail")
async def addInvoiceMasterAndInvoiceDetail(
    request: Request, db: Session = Depends(get_db)
):
    request_data = await request.json()
    InvoiceMasterDictDataList = request_data["InvoiceMaster"]
    InvoiceDetailDictDataList = request_data["InvoiceDetail"]

    # add InvoiceMaster data to database
    for InvoiceMasterDictData in InvoiceMasterDictDataList:
        InvoiceMasterDictData["Status"] = "TO_MERGE"
        InvoiceMasterPydanticData = InvoiceMasterSchema(**InvoiceMasterDictData)
        await InvoiceMasterApp.addInvoiceMaster(request, InvoiceMasterPydanticData, db)

    # add InvoiceDetail data to database
    for InvoiceDetailDictData in InvoiceDetailDictDataList:
        InvoiceDetailPydanticData = InvoiceDetailSchema(**InvoiceDetailDictData)
        await InvoiceDetailApp.addInvoiceDetail(request, InvoiceDetailPydanticData, db)

    # update InvoiceWKMaster status
    WKMasterID = InvoiceMasterDictDataList[0]["WKMasterID"]
    crud = CRUD(db, InvoiceWKMasterDBModel)
    InvoiceWKMasterData = crud.get_with_condition({"WKMasterID": WKMasterID})[0]
    InvoiceWKMasterDictData = orm_to_dict(InvoiceWKMasterData)
    InvoiceWKMasterDictData["Status"] = "BILLED"
    updatedInvoiceWKMasterData = crud.update(
        InvoiceWKMasterData, InvoiceWKMasterDictData
    )

    return {
        "message": "success add InvoiceMaster and InvoiceDetail",
        "InvoiceWKMaster status": updatedInvoiceWKMasterData.Status,
    }


# -------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------ Liability ------------------------------
@app.post(ROOT_URL + "/compareLiability")  # input data is "List[LiabilitySchema]"
async def compareLiability(request: Request, db: Session = Depends(get_db)):
    LiabilityDictDataList = await request.json()
    compareResultList = []
    crud = CRUD(db, LiabilityDBModel)
    for LiabilityDictData in LiabilityDictDataList:
        dictCondition = {
            "SubmarineCable": LiabilityDictData["SubmarineCable"],
            "WorkTitle": LiabilityDictData["WorkTitle"],
            "BillMilestone": LiabilityDictData["BillMilestone"],
            "PartyName": LiabilityDictData["PartyName"],
        }
        LiabilityDataList = crud.get_with_condition(dictCondition)
        if len(LiabilityDataList) != 0:
            for LiabilityData in LiabilityDataList:
                compareResultList.append(LiabilityData)

    if len(compareResultList) == 0:
        return {"message": "No same data", "compareResult": compareResultList}
    else:
        return {"message": "There some same datas", "compareResult": compareResultList}


@app.post(ROOT_URL + "/batchAddLiability")
async def batchAddLiability(request: Request, db: Session = Depends(get_db)):
    LiabilityDictDataList = await request.json()
    crud = CRUD(db, LiabilityDBModel)
    for LiabilityDictData in LiabilityDictDataList:
        LiabilityDictData["CreateDate"] = convert_time_to_str(datetime.now())
        LiabilityPydanticData = LiabilitySchema(**LiabilityDictData)
        crud.create(LiabilityPydanticData)
    return {"message": "success add Liability"}


# -----------------------------------------------------------------------


# ------------------------------ BillMaster & BillDetail ------------------------------
# get InvoiceMaster and InvoiceDetail data
@app.get(ROOT_URL + "/getInvoiceMaster&InvoiceDetail/{urlCondition}")
async def getInvoiceMasterAndInvoiceDetail(
    request: Request, urlCondition: str, db: Session = Depends(get_db)
):
    crudInvoiceMaster = CRUD(db, InvoiceMasterDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    getResult = []
    if "BillMilestone" in urlCondition:
        newUrlCondition, BillMilestone = re_search_url_condition_value(
            urlCondition, "BillMilestone"
        )
        dictCondition = convert_url_condition_to_dict(newUrlCondition)
        InvoiceMasterDataList = crudInvoiceMaster.get_with_condition(dictCondition)
        for InvoiceMasterData in InvoiceMasterDataList:
            InvoiceDetailDataList = crudInvoiceDetail.get_with_condition(
                {"InvMasterID": InvoiceMasterData.InvMasterID}
            )
            checkBillMilestone = list(
                filter(
                    lambda x: x.BillMilestone == BillMilestone, InvoiceDetailDataList
                )
            )
            if checkBillMilestone:
                getResult.append(
                    {
                        "InvoiceMaster": InvoiceMasterData,
                        "InvoiceDetail": InvoiceDetailDataList,
                    }
                )
    else:
        dictCondition = convert_url_condition_to_dict(urlCondition)
        InvoiceMasterDataList = crudInvoiceMaster.get_with_condition(dictCondition)
        for InvoiceMasterData in InvoiceMasterDataList:
            InvoiceDetailDataList = crudInvoiceDetail.get_with_condition(
                {"InvMasterID": InvoiceMasterData.InvMasterID}
            )
            getResult.append(
                {
                    "InvoiceMaster": InvoiceMasterData,
                    "InvoiceDetail": InvoiceDetailDataList,
                }
            )

    return getResult


@app.post(ROOT_URL + "/checkInitBillMaster&BillDetail")
async def checkInitBillMasterAndBillDetail(
    request: Request, db: Session = Depends(get_db)
):
    """
    {
        "InvoiceMaster": [
            {...},
            {...},
            {...}
        ]
    }
    """
    request_data = await request.json()
    PartyList = []
    SubmarineCableList = []
    WorkTitleList = []
    InvoiceMasterDictDataList = request_data["InvoiceMaster"]
    for InvoiceMasterDictData in InvoiceMasterDictDataList:
        PartyList.append(InvoiceMasterDictData["PartyName"])
        SubmarineCableList.append(InvoiceMasterDictData["SubmarineCable"])
        WorkTitleList.append(InvoiceMasterDictData["WorkTitle"])

    alert_msg = {}
    if len(set(PartyList)) > 1:
        alert_msg["PartyName"] = "PartyName is not unique"
    if len(set(SubmarineCableList)) > 1:
        alert_msg["SubmarineCable"] = "SubmarineCable is not unique"
    if len(set(WorkTitleList)) > 1:
        alert_msg["WorkTitle"] = "WorkTitle is not unique"
    return alert_msg


# 待抵扣階段(for 產生預覽畫面)
@app.post(ROOT_URL + "/getBillMaster&BillDetailStream")
async def initBillMasterAndBillDetail(request: Request, db: Session = Depends(get_db)):
    """
    {
        "InvoiceMaster": [
            {...},
            {...},
            {...}
        ]
    }
    """
    request_data = await request.json()
    pprint(request_data)
    InvoiceMasterIdList = [
        InvoiceMasterDictData["InvMasterID"]
        for InvoiceMasterDictData in request_data["InvoiceMaster"]
    ]

    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    crudInvoiceMaster = CRUD(db, InvoiceMasterDBModel)
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)

    InvoiceMasterDataList = crudInvoiceMaster.get_value_if_in_a_list(
        InvoiceMasterDBModel.InvMasterID, InvoiceMasterIdList
    )

    InvoiceDetailDataList = crudInvoiceDetail.get_value_if_in_a_list(
        InvoiceDetailDBModel.InvMasterID, InvoiceMasterIdList
    )
    BillingNo = f"{InvoiceMasterDataList[0].SubmarineCable}-{InvoiceMasterDataList[0].WorkTitle}-CBP-{InvoiceMasterDataList[0].PartyName}-{convert_time_to_str(datetime.now()).replace('-', '').replace(' ', '').replace(':', '')[2:-2]}"

    # change InvoiceMaster status to "MERGED"
    for InvoiceMasterData in InvoiceMasterDataList:
        InvoiceMasterDictData = orm_to_dict(InvoiceMasterData)
        InvoiceMasterDictData["Status"] = "MERGED"

    # cal FeeAmountSum
    FeeAmountSum = 0
    for InvoiceDetailData in InvoiceDetailDataList:
        FeeAmountSum += InvoiceDetailData.FeeAmountPost

    # init BillMaster
    BillMasterDictData = {
        "BillingNo": BillingNo,
        "SupplierName": InvoiceMasterDataList[0].SupplierName,
        "SubmarineCable": InvoiceMasterDataList[0].SubmarineCable,
        "WorkTitle": InvoiceMasterDataList[0].WorkTitle,
        "PartyName": InvoiceMasterDataList[0].PartyName,
        "IssueDate": convert_time_to_str(datetime.now()),
        "DueDate": None,
        "FeeAmountSum": FeeAmountSum,
        "ReceivedAmountSum": 0,
        "IsPro": InvoiceMasterDataList[0].IsPro,
        "Status": "INITIAL",
    }

    # init BillDetail
    BillDetailDataList = []
    for InvoiceDetailData in InvoiceDetailDataList:
        """
        BillDetailData keys:
        BillDetailID
        BillMasterID
        WKMasterID
        InvDetailID
        PartyName
        SupplierName
        SubmarineCable
        WorkTitle
        BillMilestone
        FeeItem
        OrgFeeAmount
        DedAmount(抵扣金額)
        FeeAmount(應收(會員繳)金額)
        ReceivedAmount(累計實收(會員繳)金額(初始為0))
        OverAmount(重溢繳金額 銷帳介面會自動計算帶出)
        ShortAmount(短繳金額 銷帳介面會自動計算帶出)
        BankFees(自行輸入)
        ShortOverReason(短繳原因 自行輸入)
        WriteOffDate(銷帳日期)
        ReceiveDate(最新收款日期 自行輸入)
        Note
        ToCB(金額是否已存在 null or Done)
        Status
        """
        BillDetailDictData = {
            # "BillMasterID": BillMasterData.BillMasterID,
            "WKMasterID": InvoiceDetailData.WKMasterID,
            "InvDetailID": InvoiceDetailData.InvDetailID,
            "PartyName": InvoiceDetailData.PartyName,
            "SupplierName": InvoiceDetailData.SupplierName,
            "SubmarineCable": InvoiceDetailData.SubmarineCable,
            "WorkTitle": InvoiceDetailData.WorkTitle,
            "BillMilestone": InvoiceDetailData.BillMilestone,
            "FeeItem": InvoiceDetailData.FeeItem,
            "OrgFeeAmount": InvoiceDetailData.FeeAmountPost,
            "DedAmount": 0,
            "FeeAmount": 0,
            "ReceivedAmount": 0,
            "OverAmount": 0,
            "ShortAmount": 0,
            "BankFees": 0,
            "ShortOverReason": None,
            "WriteOffDate": None,
            "ReceiveDate": None,
            "Note": None,
            "ToCB": None,
            "Status": "INCOMPLETE",
        }
        # BillDetailData = crudBillDetail.create(BillDetailSchema(**BillDetailDictData))
        BillDetailDataList.append(BillDetailDictData)

    return {
        "message": "success",
        "BillMaster": BillMasterDictData,
        "BillDetail": BillDetailDataList,
    }


# 待抵扣階段(for 產生初始檔存入資料庫)
@app.post(ROOT_URL + "/initBillMaster&BillDetail")
async def generateInitBillMasterAndBillDetail(
    request: Request, db: Session = Depends(get_db)
):
    request_data = await request.json()
    DueDate = request_data["DueDate"]
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    BillMasterDictData = request_data["BillMaster"]
    BillDetailDataList = request_data["BillDetail"]

    # convert BillMasterDictData to BillMasterPydanticData and insert to db
    BillMasterDictData["DueDate"] = DueDate
    BillMasterDictData["IssueDate"] = convert_time_to_str(datetime.now())
    BillMasterPydanticData = BillMasterSchema(**BillMasterDictData)
    BillMasterData = crudBillMaster.create(BillMasterPydanticData)

    newBillDetailDataList = []
    for BillDetailData in BillDetailDataList:
        BillDetailData["BillMasterID"] = BillMasterData.BillMasterID
        BillDetailPydanticData = BillDetailSchema(**BillDetailData)
        BillDetailData = crudBillDetail.create(BillDetailPydanticData)
        newBillDetailDataList.append(BillDetailData)

    return {
        "message": "success",
        "BillMaster": BillMasterData,
        "BillDetail": newBillDetailDataList,
    }


# get BillMaster and BillDetail(查詢帳單主檔&帳單明細檔)
@app.get(ROOT_URL + "/getBillMaster&BillDetail/{urlCondition}")
async def getBillMasterAndBillDetail(urlCondition: str, db: Session = Depends(get_db)):
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    getResult = []
    if urlCondition == "all":
        BillMasterDataList = crudBillMaster.get_all()
        for BillMasterData in BillMasterDataList:
            BillDetailDataList = crudBillDetail.get_with_condition(
                {"BillMasterID": BillMasterData.BillMasterID}
            )
            getResult.append(
                {
                    "BillMaster": BillMasterData,
                    "BillDetail": BillDetailDataList,
                }
            )
    else:
        dictCondition = convert_url_condition_to_dict(urlCondition)
        BillMasterDataList = crudBillMaster.get_with_condition(dictCondition)
        for BillMasterData in BillMasterDataList:
            BillDetailDataList = crudBillDetail.get_with_condition(
                {"BillMasterID": BillMasterData.BillMasterID}
            )
            getResult.append(
                {
                    "BillMaster": BillMasterData,
                    "BillDetail": BillDetailDataList,
                }
            )
    return getResult


# 已抵扣階段(for 執行抵扣，更新初始化的帳單主檔及帳單明細資料庫)
@app.post(ROOT_URL + "/generateBillMaster&BillDetail")
async def generateBillMasterAndBillDetail(
    request: Request, db: Session = Depends(get_db)
):
    """
    {
        "BillMaster": {...},
        "Deduct": [
            {
                "BillDetailID": 1,
                "CB": [
                    {
                        "CBID": 1,
                        "TransAmount": 1000
                    },
                    {...},
                    {...}
                ]
            },
            {...},
            {...}
        ]
    }
    """
    dataToBeUpdated = {
        "oldBillMasterData": None,
        "newBillMasterData": None,
        "oldCBDataList": [],
        "newCBDataList": [],
        "newCBStatementDataList" "oldBillDetailDataList": [],
        "newBillDetailDataList": [],
    }
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)
    crudCreditBalanceStatement = CRUD(db, CreditBalanceStatementDBModel)

    BillMasterDictData = (await request.json())["BillMaster"]
    BillMasterData = crudBillMaster.get_with_condition(
        {"BillMasterID": BillMasterDictData["BillMasterID"]}
    )[0]
    dataToBeUpdated["oldBillMasterData"] = BillMasterData
    deductDataList = (await request.json())["Deduct"]

    for deductData in deductDataList:
        BillDetailData = crudBillDetail.get_with_condition(
            {"BillDetailID": deductData["BillDetailID"]}
        )[0]
        dataToBeUpdated["oldBillDetailDataList"].append(BillDetailData)

        DedAmount = 0
        CBDataList = deductData["CB"]
        for CBData in CBDataList:
            CBData = crudCreditBalance.get_with_condition({"CBID": CBData["CBID"]})[0]
            dataToBeUpdated["oldCBDataList"].append(CBData)

            # update CBData and insert new CBStatementData
            TransAmount = CBData["TransAmount"] * (-1)
            DedAmount += TransAmount
            # generate new CBStatementData
            newCBStatementData = CreditBalanceStatementDBModel(
                CBID=CBData.CBID,
                BillingNo=BillMasterData.BillingNo,
                BLDetailID=BillDetailData.BillDetailID,
                TransItem="DEDUCT",
                OrgAmount=CBData.CurrAmount,
                TransAmount=TransAmount,
                Note="",
                CreateDate=convert_time_to_str(datetime.now()),
            )
            dataToBeUpdated["newCBStatementDataList"].append(newCBStatementData)

            # update CBData
            CBData.CurrAmount += TransAmount
            CBData.LastUpdDate = convert_time_to_str(datetime.now())
            dataToBeUpdated["newCBDataList"].append(CBData)

        # update BillDetailData
        BillDetailData.DedAmount = abs(DedAmount)
        BillDetailData.FeeAmount = BillDetailData.OrgFeeAmount - abs(DedAmount)
        BillDetailData.Status = bill_detail_status(
            BillDetailData.FeeAmount,
            BillDetailData.ReceivedAmount,
            BillDetailData.BankFees,
        )
        dataToBeUpdated["newBillDetailDataList"].append(BillDetailData)

    # update BillMasterData
    BillMasterData.Status = "RATED"
    dataToBeUpdated["newBillMasterData"] = BillMasterData

    # ------------------- 更新CB -------------------
    for oldCBData, newCBData in zip(
        dataToBeUpdated["oldCBDataList"], dataToBeUpdated["newCBDataList"]
    ):
        crudCreditBalance.update(oldCBData, orm_to_dict(newCBData))

    # ------------------- 新增CBStatement -------------------
    for newCBStatementData in dataToBeUpdated["newCBStatementDataList"]:
        crudCreditBalanceStatement.create(newCBStatementData)

    # ------------------- 更新BillDetail -------------------
    for oldBillDetailData, newBillDetailData in zip(
        dataToBeUpdated["oldBillDetailDataList"],
        dataToBeUpdated["newBillDetailDataList"],
    ):
        crudBillDetail.update(oldBillDetailData, orm_to_dict(newBillDetailData))

    # ------------------- 更新BillMaster -------------------
    crudBillMaster.update(
        dataToBeUpdated["oldBillMasterData"],
        orm_to_dict(dataToBeUpdated["newBillMasterData"]),
    )

    return {"message": "success", **dataToBeUpdated}


@app.get(ROOT_URL + "/getBillMaster&BillDetailWithCBData/{urlCondition}")
async def getBillMasterAndBillDetailWithCBData(
    request: Request, urlCondition: str, db: Session = Depends(get_db)
):
    getResult = list()

    table_name = "BillMaster"
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)

    # ---------- get BillMaster ----------
    if urlCondition == "all":
        BillMasterDataList = crudBillMaster.get_all()
    elif "start" in urlCondition and "end" in urlCondition:
        dictCondition = convert_url_condition_to_dict(urlCondition)
        sql_condition = convert_dict_to_sql_condition(dictCondition, table_name)
        BillMasterDataList = crudBillMaster.get_all_by_sql(sql_condition)
    else:
        dictCondition = convert_url_condition_to_dict(urlCondition)
        BillMasterDataList = crudBillMaster.get_with_condition(dictCondition)

    for BillMasterData in BillMasterDataList:
        tempDictData = {"BillMaster": BillMasterData}
        tempListData = list()
        tempBillDetailDataList = crudBillDetail.get_with_condition(
            {"BillMasterID": BillMasterData.BillMasterID}
        )
        for tempBillDetailData in tempBillDetailDataList:
            tempCBDataList = crudCreditBalance.get_with_condition(
                {"BLDetailID": tempBillDetailData.BillDetailID}
            )
            tempListData.append(
                {"BillDetail": tempBillDetailData, "CB": tempCBDataList}
            )

        tempDictData["data"] = tempListData
        getResult.append(tempDictData)

    return getResult


# 待抵扣階段退回
@app.post(ROOT_URL + "/returnBillMaster&BillDetail/beforeDeduct")
async def returnBillMasterAndBillDetail(
    request: Request, db: Session = Depends(get_db)
):
    """
    {
        "BillMaster": {},
        "ReturnStage": "VALIDATED" or "TO_MERGE"
    }
    """
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudInvoiceMaster = CRUD(db, InvoiceMasterDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)

    InvDetailIDList = []
    BillMasterDictData = (await request.json())["BillMaster"]
    ReturnStage = (await request.json())["ReturnStage"]

    # get BillDetailDataList
    BillDetailDataList = crudBillDetail.get_with_condition(
        {"BillMasterID": BillMasterDictData["BillMasterID"]}
    )
    for BillDetailData in BillDetailDataList:
        InvDetailIDList.append(BillDetailData.InvDetailID)

    InvoiceMasterDataList = crudInvoiceMaster.get_value_if_in_a_list(
        InvoiceMasterDBModel.InvDetailID, InvDetailIDList
    )

    if ReturnStage == "TO_MERGE":
        # 更新發票主檔狀態為"TO_MERGE"
        for InvoiceMasterData in InvoiceMasterDataList:
            InvoiceMasterDictData = orm_to_dict(InvoiceMasterData)
            InvoiceMasterDictData["Status"] = "TO_MERGE"
            newInvoiceMasterData = crudInvoiceMaster.update(
                InvoiceMasterData, InvoiceMasterDictData
            )
    elif ReturnStage == "VALIDATED":
        # 刪除發票主檔、發票明細檔
        for InvoiceMasterData in InvoiceMasterDataList:
            InvoiceDetailDataList = crudInvoiceDetail.get_with_condition(
                {"InvMasterID": InvoiceMasterData.InvMasterID}
            )
            for InvoiceDetailData in InvoiceDetailDataList:
                crudInvoiceDetail.remove(InvoiceDetailData.InvDetailID)
            crudInvoiceMaster.remove(InvoiceMasterData.InvMasterID)

    # 刪除BillMaster、BillDetail
    crudBillMaster.remove(BillMasterDictData["BillMasterID"])
    for BillDetailData in BillDetailDataList:
        crudBillDetail.remove(BillDetailData.BillDetailID)

    if ReturnStage == "TO_MERGE":
        return {"message": "success to return to TO_MERGE stage"}
    elif ReturnStage == "VALIDATED":
        return {"message": "success return to VALIDATED stage"}
    else:
        return {"message": "fail to return"}


# 已抵扣階段退回(選擇帳單)
@app.post(
    ROOT_URL + "/returnToValidatedBillMaster&BillDetail/afterDeduct/choiceBillMaster"
)
async def returnToValidatedBillMasterAndBillDetailChoiceBillMaster(
    request: Request, db: Session = Depends(get_db)
):
    """
    {
        "BillMaster": {},
    }
    """
    crudInvoiceWKMaster = CRUD(db, InvoiceWKMasterDBModel)
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)

    BillMasterDictData = (await request.json())["BillMaster"]
    BillMasterData = crudBillMaster.get_with_condition(
        {"BillMasterID": BillMasterDictData["BillMasterID"]}
    )[0]
    BillDetailDataList = crudBillDetail.get_with_condition(
        {"BillMasterID": BillMasterData.BillMasterID}
    )
    InvoiceWKMasterIDList = [
        BillDetailData.WKMasterID for BillDetailData in BillDetailDataList
    ]
    InvoiceWKMasterDataList = crudInvoiceWKMaster.get_value_if_in_a_list(
        InvoiceWKMasterDBModel.WKMasterID, InvoiceWKMasterIDList
    )
    return {
        "BillMaster": BillMasterData,
        "InvoiceWKMaster": InvoiceWKMasterDataList,
    }


# 已抵扣階段退回(選擇發票工作主檔)
@app.post(
    ROOT_URL
    + "/returnToValidatedBillMaster&BillDetail/afterDeduct/choiceInvoiceWKMaster"
)
async def returnToValidatedBillMasterAndBillDetailChoiceInvoiceWKMaster(
    request: Request, db: Session = Depends(get_db)
):
    """
    {
        InvoiceWKMaster: [
            {...},
            {...},
        ]
        "Confirm": True / False
        "Note": "string"
    }
    """
    crudInvoiceWKMaster = CRUD(db, InvoiceWKMasterDBModel)
    crudInvoiceMaster = CRUD(db, InvoiceMasterDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)
    crudCreditBalanceStatement = CRUD(db, CreditBalanceStatementDBModel)
    confirm = (await request.json())["Confirm"]
    note = (await request.json())["Note"]
    """
    streamResponse = [
        {
            InvoiceWKMasterData: {},
            BillMasterDataList: [
                {
                    "BillMaster": {},
                    "BillDetail": [],
                    "TotalBillDetailAmount": 123.45,
                },
                {...}
            ]
        }
    ]
    """
    InvoiceWKMasterDictDataList = (await request.json())["InvoiceWKMaster"]
    InvoiceWKMasterIDList = [
        InvoiceWKMasterData["WKMasterID"]
        for InvoiceWKMasterData in InvoiceWKMasterDictDataList
    ]
    BillDetailDataList = crudBillDetail.get_value_if_in_a_list(
        BillDetailDBModel.WKMasterID, InvoiceWKMasterIDList
    )
    BillDetailIDList = list(
        set([BillDetailData.BillDetailID for BillDetailData in BillDetailDataList])
    )
    BillMasterDataList = crudBillMaster.get_value_if_in_a_list(
        BillMasterDBModel.BillMasterID, BillDetailIDList
    )

    streamResponse = []
    for InvoiceWKMasterDictData in InvoiceWKMasterDictDataList:
        streamDictData = {
            "InvoiceWKMaster": InvoiceWKMasterDictData,
            "BillMasterDataList": [],
        }
        tempBillDetailDataList = list(
            filter(
                lambda x: x.WKMasterID == InvoiceWKMasterDictData["WKMasterID"],
                BillDetailDataList,
            )
        )
        tempBillMadterIDList = list(
            set(
                [
                    tempBillDetailData.BillMasterID
                    for tempBillDetailData in tempBillDetailDataList
                ]
            )
        )
        for tempBillMasterID in tempBillMadterIDList:
            tempBillMasterData = list(
                filter(lambda x: x.BillMasterID == tempBillMasterID, BillMasterDataList)
            )[0]
            tempBillDetailDataList = list(
                filter(lambda x: x.BillMasterID == tempBillMasterID, BillDetailDataList)
            )
            streamDictData["BillMasterDataList"].append(
                {
                    "BillMaster": tempBillMasterData,
                    "BillDetail": tempBillDetailDataList,
                }
            )
        streamResponse.append(streamDictData)
    if not confirm:
        return streamResponse
    if confirm:
        dataToBeProcessed = {
            "oldBillMasterDataList": [],
            "newBillMasterDataList": [],
            # --------------------------
            "oldBillDetailDataList": [],
            "newBillDetailDataList": [],
            # --------------------------
            "oldInvoiceWKMasterDataList": [],
            "newInvoiceWKMasterDataList": [],
            # --------------------------
            "oldCBDataList": [],
            "newCBDataList": [],
            # --------------------------
            "newCBStatementDataList": [],
        }
        for tempOldBillMasterData in BillMasterDataList:
            dataToBeProcessed["oldBillMasterDataList"].append(tempOldBillMasterData)
            tmepOldBillDetailDataList = list(
                filter(
                    lambda x: x.BillMasterID == tempOldBillMasterData.BillMasterID,
                    BillDetailDataList,
                )
            )
            FeeAmountSum = 0
            for tmepOldBillDetailData in tmepOldBillDetailDataList:
                dataToBeProcessed["oldBillDetailDataList"].append(tmepOldBillDetailData)
                tempOldCBDataList = crudCreditBalance.get_with_condition(
                    {"BLDetailID": tmepOldBillDetailData.BillDetailID}
                )
                if tempOldCBDataList:
                    # ---------------------------- CB返還 ----------------------------
                    for tempOldCBData in tempOldCBDataList:
                        tempOldCBStatementDataList = (
                            crudCreditBalanceStatement.get_with_condition(
                                {"CBID": tempOldCBData.CBID}
                            )
                        )
                        tempOldCBStatementData = max(
                            tempOldCBStatementDataList, key=lambda x: x.CreateDate
                        )
                        newCBStatementTransAmount = (
                            tempOldCBStatementData.TransAmount * (-1)
                        )
                        newCBStatementData = CreditBalanceStatementDBModel(
                            CBID=tempOldCBData.CBID,
                            BillingNo=tempOldBillMasterData.BillingNo,
                            BLDetailID=tmepOldBillDetailData.BillDetailID,
                            TransItem="RETURN",
                            OrgAmount=tempOldCBData.CurrAmount
                            + newCBStatementTransAmount,
                            TransAmount=newCBStatementTransAmount,
                            Note=note,
                            CreateDate=convert_time_to_str(datetime.now()),
                        )
                        tempNewCBData = deepcopy(tempOldCBData)
                        tempNewCBData.CurrAmount = (
                            newCBStatementData.OrgAmount
                            + newCBStatementData.TransAmount
                        )

                        # ---------------------------- BillDetail更新 ----------------------------
                        tmepOldBillDetailData.DedAmount -= newCBStatementTransAmount
                        tmepOldBillDetailData.FeeAmount = (
                            tmepOldBillDetailData.OrgFeeAmount
                            - tmepOldBillDetailData.DedAmount
                        )
                        tmepOldBillDetailData.Status = "INCOMPLETE"

                        # ---------------------------- record data to be processed ----------------------------
                        dataToBeProcessed["oldCBDataList"].append(tempOldCBData)
                        dataToBeProcessed["newCBDataList"].append(tempNewCBData)
                        dataToBeProcessed["newCBStatementDataList"].append(
                            newCBStatementData
                        )
                    dataToBeProcessed["newBillDetailDataList"].append(
                        tmepOldBillDetailData
                    )
                    FeeAmountSum += tmepOldBillDetailData.FeeAmount

            # ---------------------------- BillMaster更新 ----------------------------
            tempNewBillMasterData = deepcopy(tempOldBillMasterData)
            tempNewBillMasterData.Status = "INITIAL"
            if FeeAmountSum:
                tempNewBillMasterData.FeeAmountSum = FeeAmountSum
            dataToBeProcessed["newBillMasterDataList"].append(tempNewBillMasterData)

        # TODO: 更改發票工作主檔狀態 & 刪除發票主檔 & 發票明細檔
        InvoiceWKMasterDataList = crudInvoiceWKMaster.get_value_if_in_a_list(
            InvoiceWKMasterDBModel.WKMasterID, InvoiceWKMasterIDList
        )
        InvoiceMasterDataList = crudInvoiceMaster.get_value_if_in_a_list(
            InvoiceMasterDBModel.WKMasterID, InvoiceWKMasterIDList
        )
        InvoiceDetailDataList = crudInvoiceDetail.get_value_if_in_a_list(
            InvoiceDetailDBModel.WKMasterID, InvoiceWKMasterIDList
        )

        # ---------------------------- 更改發票工作主檔狀態 ----------------------------
        for InvoiceWKMasterData in InvoiceWKMasterDataList:
            tempNewInvoiceWKMasterData = deepcopy(InvoiceWKMasterData)
            tempNewInvoiceWKMasterData.Status = "VALIDATED"
            dataToBeProcessed["oldInvoiceWKMasterDataList"].append(InvoiceWKMasterData)
            dataToBeProcessed["newInvoiceWKMasterDataList"].append(
                tempNewInvoiceWKMasterData
            )
            crudInvoiceWKMaster.update(
                InvoiceWKMasterData, orm_to_dict(tempNewInvoiceWKMasterData)
            )
        # ---------------------------- 刪除發票主檔 & 發票明細檔 -------------------------------
        for InvoiceMasterData in InvoiceMasterDataList:
            crudInvoiceMaster.remove(InvoiceMasterData.InvMasterID)
        for InvoiceDetailData in InvoiceDetailDataList:
            crudInvoiceMaster.remove(InvoiceDetailData.InvDetailID)

        # ---------------------------- 刪除帳單主檔 & 帳單明細檔 -------------------------------
        for BillMasterData in BillMasterDataList:
            crudBillMaster.remove(BillMasterData.BillMasterID)
        for BillDetailData in BillDetailDataList:
            crudBillDetail.remove(BillDetailData.BillDetailID)

        # ---------------------------- 更新CB ----------------------------
        for oldCBdata, newCBData in zip(
            dataToBeProcessed["oldCBDataList"], dataToBeProcessed["newCBDataList"]
        ):
            crudCreditBalance.update(oldCBdata, orm_to_dict(newCBData))

        # ---------------------------- 新增CBStatement ----------------------------
        for newCBStatementData in dataToBeProcessed["newCBStatementDataList"]:
            newCBStatementPydanticData = orm_to_pydantic(
                newCBStatementData, CreditBalanceStatementSchema
            )
            crudCreditBalanceStatement.create(newCBStatementPydanticData)

        return {"message": "success", "data": dataToBeProcessed}


@app.post(ROOT_URL + "/returnToMergeBillMaster&BillDetail/afterDeduct")
async def returnToMergeBillMasterAndBillDetailAfterDeduct(
    request: Request, db: Session = Depends(get_db)
):
    dataToBeProcessed = {
        "oldCBDataList": list(),
        "newCBDataList": list(),
        "newCBStatementDataList": list(),
    }

    crudInvoiceMaster = CRUD(db, InvoiceMasterDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)
    crudCreditBalanceStatement = CRUD(db, CreditBalanceStatementDBModel)

    BillMasterDictData = await request.json()

    # ---------------------- get BillMaster data ----------------------
    BillMasterData = crudBillMaster.get_with_condition(
        {"BillMasterID": BillMasterDictData["BillMasterID"]}
    )[0]

    # ---------------------- get BillDetail data ----------------------
    BillDetailDataList = crudBillDetail.get_with_condition(
        {"BillMasterID": BillMasterData.BillMasterID}
    )

    # ---------------------- get CB data ----------------------
    CBDataList = crudCreditBalance.get_value_if_in_a_list(
        CreditBalanceDBModel.BLDetailID, [x.BillDetailID for x in BillDetailDataList]
    )

    # ---------------------- get CBStatement data ----------------------
    CBStatementDataList = crudCreditBalanceStatement.get_value_if_in_a_list(
        CreditBalanceStatementDBModel.CBID, [x.CBID for x in CBDataList]
    )

    for BillDetailData in BillDetailDataList:
        tempOldCBDataList = list(
            filter(lambda x: x.BLDetailID == BillDetailData.BillDetailID, CBDataList)
        )
        for tempOldCBData in tempOldCBDataList:
            tempOldCBStatementDataList = list(
                filter(lambda x: x.CBID == tempOldCBData.CBID, CBStatementDataList)
            )
            tempOldCBStatementData = max(
                tempOldCBStatementDataList, key=lambda x: x.CreateDate
            )
            newCBStatementTransAmount = tempOldCBStatementData.TransAmount * (-1)
            newCBStatementData = CreditBalanceStatementDBModel(
                CBID=tempOldCBData.CBID,
                BillingNo=BillMasterData.BillingNo,
                BLDetailID=BillDetailData.BillDetailID,
                TransItem="RETURN",
                OrgAmount=tempOldCBData.CurrAmount + newCBStatementTransAmount,
                TransAmount=newCBStatementTransAmount,
                Note="",
                CreateDate=convert_time_to_str(datetime.now()),
            )
            tempNewCBData = deepcopy(tempOldCBData)
            tempNewCBData.CurrAmount = (
                newCBStatementData.OrgAmount + newCBStatementData.TransAmount
            )

            dataToBeProcessed["oldCBDataList"].append(tempOldCBData)
            dataToBeProcessed["newCBDataList"].append(tempNewCBData)
            dataToBeProcessed["newCBStatementDataList"].append(newCBStatementData)

    # ---------------------------- 刪除帳單主檔 & 帳單明細檔 -------------------------------
    crudBillMaster.remove(BillMasterData.BillMasterID)
    for BillDetailData in BillDetailDataList:
        crudBillDetail.remove(BillDetailData.BillDetailID)

    # ---------------------------- 更新InvoiceMaster狀態 -------------------------------
    InvDetailIDList = [
        BillDetailData.InvDetailID for BillDetailData in BillDetailDataList
    ]
    InvoiceDetailDataList = crudInvoiceDetail.get_value_if_in_a_list(
        InvoiceDetailDBModel.InvDetailID, InvDetailIDList
    )
    InvMasterIDList = [
        InvoiceDetailData.InvMasterID for InvoiceDetailData in InvoiceDetailDataList
    ]
    InvMasterDataList = crudInvoiceMaster.get_value_if_in_a_list(
        InvoiceMasterDBModel.InvMasterID, InvMasterIDList
    )
    for InvMasterData in InvMasterDataList:
        newInvMasterDictData = orm_to_dict(InvMasterData)
        newInvMasterDictData["Status"] = "TO_MERGE"
        crudInvoiceMaster.update(InvMasterData, newInvMasterDictData)

    # ---------------------------- 更新CB -------------------------------
    for oldCBData, newCBData in zip(
        dataToBeProcessed["oldCBDataList"], dataToBeProcessed["newCBDataList"]
    ):
        crudCreditBalance.update(oldCBData, orm_to_dict(newCBData))

    # ---------------------------- 新增CBStatement -------------------------------
    for newCBStatementData in dataToBeProcessed["newCBStatementDataList"]:
        newCBStatementPydanticData = orm_to_pydantic(
            newCBStatementData, CreditBalanceStatementSchema
        )
        crudCreditBalanceStatement.create(newCBStatementPydanticData)

    return {"message": "success"}


@app.post(ROOT_URL + "/returnToInitialBillMaster&BillDetail/afterDeduct")
async def returnToInitialBillMasterAndBillDetailAfterDeduct(
    request: Request, db: Session = Depends(get_db)
):
    dataToBeProcessed = {
        "oldBillMasterDataList": [],
        "newBillMasterDataList": [],
        # --------------------------
        "oldBillDetailDataList": [],
        "newBillDetailDataList": [],
        # --------------------------
        "oldCBDataList": [],
        "newCBDataList": [],
        # --------------------------
        "newCBStatementDataList": [],
    }
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)
    crudCreditBalanceStatement = CRUD(db, CreditBalanceStatementDBModel)

    BillMasterDictData = await request.json()
    BillMasterData = crudBillMaster.get_with_condition(
        {"BillMasterID": BillMasterDictData["BillMasterID"]}
    )[0]
    dataToBeProcessed["oldBillMasterDataList"].append(BillMasterData)
    BillDetailDataList = crudBillDetail.get_with_condition(
        {"BillMasterID": BillMasterData.BillMasterID}
    )
    BillDetailIDList = [
        BillDetailData.BillDetailID for BillDetailData in BillDetailDataList
    ]
    CBDataList = crudCreditBalance.get_value_if_in_a_list(
        CreditBalanceDBModel.BLDetailID, BillDetailIDList
    )
    CBIDList = [CBData.CBID for CBData in CBDataList]
    CBStatementDataList = crudCreditBalanceStatement.get_value_if_in_a_list(
        CreditBalanceStatementDBModel.CBID, CBIDList
    )
    dataToBeProcessed["oldBillDetailDataList"].extend(BillDetailDataList)
    FeeAmountSum = 0
    for BillDetailData in BillDetailDataList:
        tempOldCBDataList = list(
            filter(lambda x: x.BLDetailID == BillDetailData.BillDetailID, CBDataList)
        )
        for tempOldCBData in tempOldCBDataList:
            tempOldCBStatementDataList = list(
                filter(lambda x: x.CBID == tempOldCBData.CBID, CBStatementDataList)
            )
            tempOldCBStatementData = max(
                tempOldCBStatementDataList, key=lambda x: x.CreateDate
            )
            newCBStatementTransAmount = tempOldCBStatementData.TransAmount * (-1)
            newCBStatementData = CreditBalanceStatementDBModel(
                CBID=tempOldCBData.CBID,
                BillingNo=BillMasterData.BillingNo,
                BLDetailID=BillDetailData.BillDetailID,
                TransItem="RETURN",
                OrgAmount=tempOldCBData.CurrAmount + newCBStatementTransAmount,
                TransAmount=newCBStatementTransAmount,
                Note="",
                CreateDate=convert_time_to_str(datetime.now()),
            )
            tempNewCBData = deepcopy(tempOldCBData)
            tempNewCBData.CurrAmount = (
                newCBStatementData.OrgAmount + newCBStatementData.TransAmount
            )
            # ---------------------------- BillDetail更新 ----------------------------
            BillDetailData.DedAmount -= newCBStatementTransAmount
            BillDetailData.FeeAmount = (
                BillDetailData.OrgFeeAmount - BillDetailData.DedAmount
            )
            BillDetailData.Status = "INCOMPLETE"

            # ---------------------------- record data to be processed ----------------------------
            dataToBeProcessed["oldCBDataList"].append(tempOldCBData)
            dataToBeProcessed["newCBDataList"].append(tempNewCBData)
            dataToBeProcessed["newCBStatementDataList"].append(newCBStatementData)
        dataToBeProcessed["newBillDetailDataList"].append(BillDetailData)
        FeeAmountSum += BillDetailData.FeeAmount

    BillMasterData.Status = "INITIAL"
    if FeeAmountSum:
        BillMasterData.FeeAmountSum = FeeAmountSum
    dataToBeProcessed["newBillMasterDataList"].append(BillMasterData)

    # ---------------------------- 更新BillMaster -------------------------------
    for oldBillMasterData, newBillMasterData in zip(
        dataToBeProcessed["oldBillMasterDataList"],
        dataToBeProcessed["newBillMasterDataList"],
    ):
        crudBillMaster.update(oldBillMasterData, orm_to_dict(newBillMasterData))

    # ---------------------------- 更新BillDetail -------------------------------
    for oldBillDetailData, newBillDetailData in zip(
        dataToBeProcessed["oldBillDetailDataList"],
        dataToBeProcessed["newBillDetailDataList"],
    ):
        crudBillDetail.update(oldBillDetailData, orm_to_dict(newBillDetailData))

    # ---------------------------- 更新CB -------------------------------
    for oldCBData, newCBData in zip(
        dataToBeProcessed["oldCBDataList"], dataToBeProcessed["newCBDataList"]
    ):
        crudCreditBalance.update(oldCBData, orm_to_dict(newCBData))

    # ---------------------------- 新增CBStatement -------------------------------
    for newCBStatementData in dataToBeProcessed["newCBStatementDataList"]:
        newCBStatementPydanticData = orm_to_pydantic(
            newCBStatementData, CreditBalanceStatementSchema
        )
        crudCreditBalanceStatement.create(newCBStatementPydanticData)
    return {"message": "success"}


# check input BillingNo is existed or not
@app.get(ROOT_URL + "/checkBillingNo/{BillingNo}")
async def checkBillingNo(request: Request, db: Session = Depends(get_db)):
    BillingNo = request.path_params["BillingNo"]
    crud = CRUD(db, BillMasterDBModel)
    BillMasterDataList = crud.get_with_condition({"BillingNo": BillingNo})
    if not BillMasterDataList:
        return {"message": "BillingNo is not exist"}
    else:
        return {"message": "BillingNo is exist"}


# 產製帳單draft(初始化)
@app.post(ROOT_URL + "/getBillMasterDraftStream")
async def getBillMasterDraftStream(request: Request, db: Session = Depends(get_db)):
    """
    {
      "BillMasterID": 1,
      "UserName": "username",
    }
    """
    getResult = {}
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudCorporates = CRUD(db, CorporatesDBModel)
    crudUsers = CRUD(db, UsersDBModel)

    # --------------------------- 抓取帳單主檔及帳單明細 ---------------------------
    BillMasterData = crudBillMaster.get_with_condition(
        {"BillMasterID": request.json()["BillMasterID"]}
    )[0]
    BillDetailDataList = crudBillDetail.get_with_condition(
        {"BillMasterID": BillMasterData.BillMasterID}
    )

    # --------------------------- 抓取聯盟資料表(含金融帳戶資訊) ---------------------------
    CorporateData = crudCorporates.get_with_condition(
        {"SubmarineCable": BillMasterData.SubmarineCable}
    )[0]

    # --------------------------- 抓取使用者資料 ---------------------------
    UserData = crudUsers.get_with_condition(
        {"UserName": request.json()["UserName"]}
    )[0]

    ContactWindowAndSupervisorInformationDictData = {
        "Company": UserData.Company,
        "Address": UserData.Address,
        "Tel":
    }






    return getResult


@app.get(ROOT_URL + "/test")
async def test(request: Request, db: Session = Depends(get_db)):
    crud = CRUD(db, InvoiceWKMasterDBModel)
    InvoiceWKMasterData = crud.get_all()[0]
    InvoiceWKMasterDictData = orm_to_dict(InvoiceWKMasterData)
    crud.update(InvoiceWKMasterData, InvoiceWKMasterDictData)
    InvoiceWKMasterData = dict_to_orm(InvoiceWKMasterDictData, InvoiceWKMasterDBModel)
    return {"message": "test", "InvoiceWKMasterData": InvoiceWKMasterData}


# -------------------------------------------------------------------------------------
