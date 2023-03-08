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
from service.CBPBankAccount.app import router as CBPBankAccountRouter
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
app.include_router(CBPBankAccountRouter, prefix=ROOT_URL, tags=["CBPBankAccount"])
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
                f"SubmarineCable={SubmarineCable}&WorkTitle={WorkTitle}&BillMilestone={InvoiceWKDetailDictData.get('BillMilestone')}",
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
    getResult = []
    if urlCondition != "all":
        if "BillMilestone" in urlCondition:
            urlCondition, BillMilestone = re_search_url_condition_value(
                urlCondition, "BillMilestone"
            )
        InvoiceMasterDataList = await InvoiceMasterApp.getInvoiceMaster(
            request, urlCondition, db
        )
        # TODO: Start to get InvoiceDetail data
        for InvoiceMasterData in InvoiceMasterDataList:
            InvoiceDetailDataList = await InvoiceDetailApp.getInvoiceDetail(
                request, f"InvMasterID={InvoiceMasterData.InvMasterID}", db
            )
            getResult.append(
                {
                    "InvoiceMaster": InvoiceMasterData,
                    "InvoiceDetail": InvoiceDetailDataList,
                }
            )
        if "BillMilestone" in urlCondition:
            InvMasterIDList = [
                data["InvoiceMaster"].InvMasterID
                for data in getResult
                for InvoiceDetailData in data["InvoiceDetail"]
                if InvoiceDetailData.BillMilestone == BillMilestone
            ]
        else:
            InvMasterIDList = [data["InvoiceMaster"].InvMasterID for data in getResult]
        InvMasterIDList = list(set(InvMasterIDList))
        getResult = [
            data
            for data in getResult
            if data["InvoiceMaster"].InvMasterID in InvMasterIDList
        ]
    else:
        InvoiceMasterDataList = await InvoiceMasterApp.getInvoiceMaster(
            request, urlCondition, db
        )
        for InvoiceMasterData in InvoiceMasterDataList:
            InvoiceDetailDataList = await InvoiceDetailApp.getInvoiceDetail(
                request, f"InvMasterID={InvoiceMasterData.InvMasterID}", db
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
        "BillingNo": "testNo.",
        "IssueDate": "2021-01-01",
        "DueDate": "2021-01-02",
        "InvoiceMaster": [
            {...},
            {...},
            {...}
        ]
    }
    """
    request_data = await request.json()
    InvoiceMasterIdList = [
        InvoiceMasterDictData["InvMasterID"]
        for InvoiceMasterDictData in request_data["InvoiceMaster"]
    ]
    BillingNo = request_data["BillingNo"]
    DueDate = request_data["DueDate"]
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

    # change InvoiceMaster status to "MERGED"
    for InvoiceMasterData in InvoiceMasterDataList:
        InvoiceMasterDictData = orm_to_dict(InvoiceMasterData)
        InvoiceMasterDictData["Status"] = "MERGED"
        newInvoiceMasterData = crudInvoiceMaster.update(
            InvoiceMasterData, InvoiceMasterDictData
        )

    # cal FeeAmountSum
    FeeAmountSum = 0
    for InvoiceDetailData in InvoiceDetailDataList:
        FeeAmountSum += InvoiceDetailData.FeeAmountPost

    # init BillMaster
    BillMasterDictData = {
        "BillingNo": BillingNo,
        "SubmarineCable": InvoiceMasterDataList[0].SubmarineCable,
        "WorkTitle": InvoiceMasterDataList[0].WorkTitle,
        "PartyName": InvoiceMasterDataList[0].PartyName,
        "IssueDate": convert_time_to_str(datetime.now()),
        "DueDate": DueDate,
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
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    BillMasterDictData = request_data["BillMaster"]
    BillDetailDataList = request_data["BillDetail"]

    # convert BillMasterDictData to BillMasterPydanticData and insert to db
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
        "BillDetail": [
            {...},
            {...},
        ]
        "CB": [
            {
                "CBID": 1,
                TransAmount: 1000,
            }

        ]

    }
    """
    request_data = await request.json()
    BillDetailDictDataList = request_data["BillDetail"]
    BillMasterDictData = request_data["BillMaster"]
    CBList = request_data["CB"]

    # init crud
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)
    crudCBStatement = CRUD(db, CreditBalanceStatementDBModel)

    # 開始做抵扣
    FeeAmountSum = 0
    newBillDetailDataList = []
    newCBStatementDataList = []
    newCBList = []
    for info in BillDetailDictDataList:
        InvDetailID = info["InvDetailID"]
        DedAmount = sum([CB["TransAmount"] for CB in CBList])
        BillDetailData = crudBillDetail.get_with_condition(
            {"InvDetailID": InvDetailID}
        )[0]
        BillDetailDictData = orm_to_dict(BillDetailData)
        BillDetailDictData["DedAmount"] = DedAmount
        BillDetailDictData["FeeAmount"] = (
            BillDetailDictData["OrgFeeAmount"] - BillDetailDictData["DedAmount"]
        )
        BillDetailDictData["Status"] = bill_detail_status(
            BillDetailDictData["FeeAmount"],
            BillDetailDictData["ReceivedAmount"],
            BillDetailDictData["BankFees"],
        )
        FeeAmountSum += BillDetailDictData["FeeAmount"]

        # insert to DB
        BillDetailData = crudBillDetail.update(BillDetailData, BillDetailDictData)
        newBillDetailDataList.append(BillDetailData)

        # update CB and generate CBStatement
        for CB in CBList:
            # update CB
            CreditBalanceData = crudCreditBalance.get_with_condition(
                {"CBID": CB["CBID"]}
            )[0]
            CreditBalanceDictData = orm_to_dict(CreditBalanceData)
            OrgAmount = CreditBalanceDictData["CurrAmount"]
            CreditBalanceDictData["CurrAmount"] -= CB["TransAmount"]
            CreditBalanceDictData["LastUpDate"] = convert_time_to_str(datetime.now())
            newCreditBalanceData = crudCreditBalance.update(
                CreditBalanceData, CreditBalanceDictData
            )  # insert to DB
            newCBList.append(newCreditBalanceData)

            # generate CBStatement
            CBStatementDictData = {
                "CBID": CB["CBID"],
                "BillingNo": BillMasterDictData["BillingNo"],
                "BLDetailID": BillDetailData.BillDetailID,
                "TransItem": "DEDUCT",  # 帳單金額抵扣
                "OrgAmount": OrgAmount,
                "TransAmount": CB["TransAmount"] * -1,
                "Note": None,
                "CreateDate": convert_time_to_str(datetime.now()),
            }
            CBStatementPydanticData = CreditBalanceStatementSchema(
                **CBStatementDictData
            )
            CBStatementData = crudCBStatement.create(CBStatementPydanticData)
            newCBStatementDataList.append(CBStatementData)

    BillMasterData = crudBillMaster.get_with_condition(
        {"BillMasterID": BillMasterDictData["BillMasterID"]}
    )[0]
    BillMasterDictData["FeeAmountSum"] = FeeAmountSum
    BillMasterDictData["Status"] = "RATED"
    newBillMasterData = crudBillMaster.update(BillMasterData, BillMasterDictData)
    return {
        "message": "success",
        "BillMaster": newBillMasterData,
        "BillDetail": newBillDetailDataList,
        "CBStatement": newCBStatementDataList,
        "CB": newCBList,
    }


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


# 已抵扣階段退回
@app.post(ROOT_URL + "/returnToValidatedBillMaster&BillDetail/afterDeduct")
async def returnToValidatedBillMasterAndBillDetail(
    request: Request, db: Session = Depends(get_db)
):
    """
    {
        "BillMaster": {},
        "ReturnStage": "VALIDATED" or "TO_MERGE" or "INITIAL"
        "Note": "Reason for return"
        "ConfirmExecute": "Y" or "N
    }
    """
    BillMasterDictData = (await request.json())["BillMaster"]
    Note = (await request.json())["Note"]
    crudInvoiceMaster = CRUD(db, InvoiceMasterDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)
    crudCreditBalanceStatement = CRUD(db, CreditBalanceStatementDBModel)
    recordProcessing = {
        # -----------------------------
        "InvoiceMaster": list(),
        "InvoiceDetail": list(),
        # -----------------------------
        "originalBillMaster": list(),
        "originalBillDetail": list(),
        "newBillDetail": list(),
        # -----------------------------
        "originalCreditBalance": list(),
        "newCreditBalance": list(),
        # -----------------------------
        "newCBStatement": list(),
    }

    BillDetailDataList = crudBillDetail.get_with_condition(
        {"BillMasterID": BillMasterDictData["BillMasterID"]}
    )

    # ----- 抓取發票明細檔ID -----
    InvDetailIDList = [
        BillDetailData.InvDetailID for BillDetailData in BillDetailDataList
    ]

    # ----- 抓取發票明細檔 -----
    InvoiceDetailDataList = crudInvoiceDetail.get_value_if_in_a_list(
        InvoiceDetailDBModel.InvDetailID, InvDetailIDList
    )
    InvWKMasterIDList = unique_list(
        [InvoiceDetailData.InvWKMasterID for InvoiceDetailData in InvoiceDetailDataList]
    )
    InvoiceDetailDataList = crudInvoiceDetail.get_value_if_in_a_list(
        InvoiceDetailDBModel.InvWKMasterID, InvWKMasterIDList
    )
    recordProcessing["InvoiceDetail"].extend(InvoiceDetailDataList)

    # ----- 重新抓取發票明細檔ID -----
    InvDetailIDList = [
        InvoiceDetailData.InvDetailID for InvoiceDetailData in InvoiceDetailDataList
    ]

    # ----- 抓取所有帳單明細檔 -----
    BillDetailDataList = crudBillDetail.get_value_if_in_a_list(
        BillDetailDBModel.InvDetailID, InvDetailIDList
    )

    # ----- 抓取所有帳單主檔 -----
    BillMasterIDList = unique_list(
        [BillDetailData.BillMasterID for BillDetailData in BillDetailDataList]
    )
    BillMasterDataList = crudBillMaster.get_value_if_in_a_list(
        BillMasterDBModel.BillMasterID, BillMasterIDList
    )
    recordProcessing["originalBillMaster"].extend(BillMasterDataList)
    for BillMasterData in BillMasterDataList:
        tempBillDetailDataList = list(
            filter(
                lambda x: x.BillMasterID == BillMasterData.BillMasterID,
                BillDetailDataList,
            )
        )
        for tempBillDetailData in tempBillDetailDataList:
            originalTempBillDetailData = deepcopy(tempBillDetailData)
            recordProcessing["originalBillDetail"].append(originalTempBillDetailData)
            tempCBDataList = crudCreditBalance.get_with_condition(
                {"InvDetailID": tempBillDetailData.InvDetailID}
            )
            if tempCBDataList:  # 如果有抵扣紀錄
                recordProcessing["originalCreditBalance"].extend(tempCBDataList)
                for tempCBData in tempCBDataList:
                    tempCBDetailData = crudCreditBalanceStatement.get_with_condition(
                        {"CreditBalanceID": tempCBData.CreditBalanceID}
                    )[0]
                    tempTransAmount = abs(tempCBDetailData.TransAmount)
                    tempBillDetailData.DedAmount -= tempTransAmount
                    tempCBData.CurrAmount += tempTransAmount
                    recordProcessing["newCreditBalance"].append(tempCBData)
                    newCBStatementDictData = {
                        "CBID": tempCBData.CBID,
                        "BillingNo": BillMasterData.BillingNo,
                        "BLDetailID": tempBillDetailData.BillDetailID,
                        "TransItem": "RETURN",  # 帳單作廢金額返還
                        "OrgAmount": tempCBData.CurrAmount - tempTransAmount,
                        "TransAmount": tempTransAmount,
                        "Note": Note,
                        "CreateDate": convert_time_to_str(datetime.now()),
                    }
                    recordProcessing["newCBStatement"].append(newCBStatementDictData)
            # 變更帳單明細檔狀態、應收(會員繳)金額
            tempBillDetailData.BillStatus = "INCOMPLETE"
            tempBillDetailData.FeeAmount = tempBillDetailData.OrgFeeAmount
            recordProcessing["newBillDetail"].append(tempBillDetailData)
    InvoiceMasterDataList = crudInvoiceMaster.get_value_if_in_a_list(
        InvoiceMasterDBModel.InvWKMasterID, InvWKMasterIDList
    )
    recordProcessing["InvoiceMaster"].extend(InvoiceMasterDataList)
    # TODO : 把變更的資料或要新增或刪除的資料寫入資料庫
    return recordProcessing


@app.post(ROOT_URL + "/returnToMergeBillMasterAndBillDetail/afterDeduct")
async def returnToMergeBillMasterAndBillDetailAfterDeduct(
    request: Request, db: Session = Depends(get_db)
):
    """
    {
        "BillMaster": {},
        "ReturnStage": "VALIDATED" or "TO_MERGE" or "INITIAL"
        "Note": "Reason for return"
        "ConfirmExecute": "Y" or "N
    }
    """
    BillMasterDictData = (await request.json())["BillMaster"]
    Note = (await request.json())["Note"]
    crudInvoiceMaster = CRUD(db, InvoiceMasterDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)
    crudCreditBalanceStatement = CRUD(db, CreditBalanceStatementDBModel)
    recordProcessing = {
        "origBillMaster": BillMasterDictData,
        # -----------------------------
        "origBillDetail": list(),
        "newBillDetail": list(),
        # -----------------------------
        "origiCreditBalance": list(),
        "newCreditBalance": list(),
        # -----------------------------
        "newCBStatement": list(),
    }
    BillDetailDataList = crudBillDetail.get_with_condition(
        {"BillMasterID": BillMasterDictData["BillMasterID"]}
    )
    recordProcessing["origBillDetail"].extend(BillDetailDataList)

    for tempBillDetailData in BillDetailDataList:
        tempCBDataList = crudCreditBalance.get_with_condition(
            {"InvDetailID": tempBillDetailData.InvDetailID}
        )
        for tempCBData in tempCBDataList:
            origTempCBData = deepcopy(tempCBData)
            tempCBStatementData = crudCreditBalanceStatement.get_with_condition(
                {"CBID": tempCBData.CBID}
            )[0]
            tempBillDetailData.DedAmount -= abs(tempCBStatementData.TransAmount)
            tempCBData.CurrAmount += abs(tempCBStatementData.TransAmount)
            newCBStatementDictData = {
                "CBID": tempCBData.CBID,
                "BillingNo": BillMasterDictData["BillingNo"],
                "BLDetailID": tempBillDetailData.BillDetailID,
                "TransItem": "RETURN",  # 帳單作廢金額返還
                "OrgAmount": tempCBData.CurrAmount - abs(tempCBStatementData.TransAmount),
                "TransAmount": abs(tempCBStatementData.TransAmount),
                "Note": Note,
                "CreateDate": convert_time_to_str(datetime.now()),
            }
            recordProcessing["origiCreditBalance"].append(origTempCBData)
            recordProcessing["newCreditBalance"].append(tempCBData)
            recordProcessing["newCBStatement"].append(newCBStatementDictData)
        tempBillDetailData.BillStatus = "INCOMPLETE"
        tempBillDetailData.FeeAmount = tempBillDetailData.OrgFeeAmount
        recordProcessing["newBillDetail"].append(tempBillDetailData)




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


# -------------------------------------------------------------------------------------
