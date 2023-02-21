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
    BillMilestoneValue = None
    checkBillMilestoneInvoiceWKDetailDictDataList = None
    if "BillMilestone" in urlCondition:
        urlCondition, BillMilestoneValue = re_search_url_condition_value(
            urlCondition, "BillMilestone"
        )

    # get InvoiceWKMaster
    InvoiceWKMasterDataList = await InvoiceWKMasterApp.getInvoiceWKMaster(
        request, urlCondition, db
    )

    InvoiceWKMasterDictDataList = [
        orm_to_pydantic(InvoiceWKMasterData, InvoiceWKMasterSchema).dict()
        for InvoiceWKMasterData in InvoiceWKMasterDataList
    ]

    # 只查詢 TEMPORARY 和 VALIDATED 的資料(篩選)
    if "Status" not in urlCondition:
        newInvoiceWKMasterDictDataList = []
        for InvoiceWKMasterDictData in InvoiceWKMasterDictDataList:
            # TODO: 這邊要改成所有的狀態都要顯示
            # if (
            #     InvoiceWKMasterDictData["Status"] == "TEMPORARY"
            #     or InvoiceWKMasterDictData["Status"] == "VALIDATED"
            # ):
            #     newInvoiceWKMasterDictDataList.append(InvoiceWKMasterDictData)
            newInvoiceWKMasterDictDataList.append(InvoiceWKMasterDictData)
        InvoiceWKMasterDictDataList = newInvoiceWKMasterDictDataList

    # get InvoiceWKDetail
    for InvoiceWKMasterDictData in InvoiceWKMasterDictDataList:
        InvoiceWKDetailDataList = await InvoiceWKDetailApp.getInvoiceWKDetail(
            request, f"WKMasterID={InvoiceWKMasterDictData.get('WKMasterID')}", db
        )
        InvoiceWKDetailDictDataList = [
            orm_to_pydantic(InvoiceWKDetailData, InvoiceWKDetailSchema).dict()
            for InvoiceWKDetailData in InvoiceWKDetailDataList
        ]
        newInvoiceWKDetailDictDataList = []
        for InvoiceWKDetailDictData in InvoiceWKDetailDictDataList:
            InvoiceWKDetailDictData.pop("WKDetailID")
            newInvoiceWKDetailDictDataList.append(InvoiceWKDetailDictData)
        InvoiceWKDetailDictDataList = newInvoiceWKDetailDictDataList
        # generate InvoiceMaster & InvoiceDetail result
        InvoiceWKMasterDictData = convert_dict_data_date_to_normal_str(
            InvoiceWKMasterDictData
        )

        # filter BillMilestone
        if BillMilestoneValue:
            checkBillMilestoneInvoiceWKDetailDictDataList = [
                InvoiceWKDetailData
                for InvoiceWKDetailData in InvoiceWKDetailDictDataList
                if InvoiceWKDetailData["BillMilestone"] == BillMilestoneValue
            ]
            if checkBillMilestoneInvoiceWKDetailDictDataList:
                getResult.append(
                    {
                        "InvoiceWKMaster": InvoiceWKMasterDictData,
                        "InvoiceWKDetail": InvoiceWKDetailDictDataList,
                    }
                )
        else:
            getResult.append(
                {
                    "InvoiceWKMaster": InvoiceWKMasterDictData,
                    "InvoiceWKDetail": InvoiceWKDetailDictDataList,
                }
            )

    return getResult


@app.get(ROOT_URL + "/getInvoiceMaster&InvoiceDetailStream/WKMasterID={WKMasterID}")
async def getInvoiceMasterInvoiceDetailStram(
    request: Request,
    WKMasterID: int,
    db: Session = Depends(get_db),
):
    # Step1. Get InvoiceWKMaster
    InvoiceWKMasterDataList = await InvoiceWKMasterApp.getInvoiceWKMaster(
        request, f"WKMasterID={WKMasterID}", db
    )
    # print(InvoiceWKMasterDataList)
    InvoiceWKMasterData = InvoiceWKMasterDataList[0]
    InvoiceWKMasterDictData = orm_to_pydantic(
        InvoiceWKMasterData, InvoiceWKMasterSchema
    ).dict()
    TotalAmount = InvoiceWKMasterDictData.get("TotalAmount")
    WorkTitle = InvoiceWKMasterDictData["WorkTitle"]
    SubmarineCable = InvoiceWKMasterDictData["SubmarineCable"]
    # pprint(InvoiceWKMasterDictData)

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

    print(len(InvoiceDetailDictDataList))
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


@app.post(ROOT_URL + "/initBillMaster&BillDetail")
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

    # cal FeeAmountSum
    FeeAmountSum = 0
    for InvoiceDetailData in InvoiceDetailDataList:
        FeeAmountSum += InvoiceDetailData.FeeAmountPost

    # init BillMaster
    BillMasterDictData = {
        "BillingNo": BillingNo,
        "PartyName": InvoiceMasterDataList[0].PartyName,
        "IssueDate": convert_time_to_str(datetime.now()),
        "DueDate": DueDate,
        "FeeAmountSum": FeeAmountSum,
        "ReceivedAmountSum": 0,
        "IsPro": InvoiceMasterDataList[0].IsPro,
        "Status": "INITIAL",
    }

    # insert BillMaster to DB
    crudBillMaster = CRUD(db, BillMasterDBModel)
    BillMasterPydanticData = BillMasterSchema(**BillMasterDictData)
    BillMasterData = crudBillMaster.create(BillMasterPydanticData)
    print(BillMasterDictData)

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
            "BillMasterID": BillMasterData.BillMasterID,
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
            "WriteOffDate": None,
            "ReceiveDate": None,
            "Note": None,
            "ToCB": None,
            "Status": "INITIAL",
        }
        BillDetailData = crudBillDetail.create(BillDetailSchema(**BillDetailDictData))
        BillDetailDataList.append(BillDetailData)

    return {
        "message": "success",
        "BillMaster": BillMasterData,
        "BillDetailDataList": BillDetailDataList,
    }


@app.post(ROOT_URL + "/generateBillMaster&BillDetail")
async def generateBillMasterAndBillDetail(
    request: Request, db: Session = Depends(get_db)
):
    """
    {
        "BillMaster": {...},
        "BillDetailDataList": [
            {
                "InvDetailID": "1",
                "CBList": [
                    {
                        "CBID": "1",
                        "TransAmount": 1000,
                    },
                    {...},
                    {...},
                ]
            },
            {...},
            {...}
        ]
    }
    """
    request_data = await request.json()
    BillDetailDictDataList = request_data["BillDetailDataList"]

    # init crud
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)

    # 開始做抵扣
    for info in BillDetailDictDataList:
        InvDetailID = info["InvDetailID"]
        CreditBalanceIdList = [CB["CBID"] for CB in info["CBList"]]
        CreditBalanceDataList = crudCreditBalance.get_value_if_in_a_list(
            CreditBalanceDBModel.CBID, CreditBalanceIdList
        )
        DedAmount = [CB["TransAmount"] for CB in info["CBList"]]
        BillDetailData = crudBillDetail.get_with_condition(
            {"InvDetailID": InvDetailID}
        )[0]
        BillDetailDictData = orm_to_dict(BillDetailData)
        BillDetailDictData["DedAmount"] = DedAmount
        BillDetailDictData["FeeAmount"] = (
            BillDetailDictData["OrgFeeAmount"] - BillDetailDictData["DedAmount"]
        )

    pass


@app.get(
    ROOT_URL + "/checkBillingNo/{BillingNo}"
)  # check input BillingNo is existed or not
async def checkBillingNo(request: Request, db: Session = Depends(get_db)):
    BillingNo = request.path_params["BillingNo"]
    print(BillingNo)
    crud = CRUD(db, BillMasterDBModel)
    BillMasterDataList = crud.get_with_condition({"BillingNo": BillingNo})
    if not BillMasterDataList:
        return {"message": "BillingNo is not exist"}
    else:
        return {"message": "BillingNo is exist"}


# @app.router.get(ROOT_URL + "/Test/{condition}")
# async def Test(request: Request, db: Session = Depends(get_db)):
#     condition = request.path_params["condition"]
#     crud = CRUD(db, InvoiceWKMasterDBModel)
#     dict_condition = convert_url_condition_to_dict(condition)
#     print(dict_condition)
#     dataList = crud.get_with_condition(dict_condition)
#     print(dataList[0].IsPro)
#     print(dataList[0].__dict__)
#     dictData = deepcopy(dataList[0].__dict__)
#     df = pd.DataFrame.from_dict(dictData, orient="index").T
#     print(df)
#     print(type(df))
#     df.to_csv("test.csv", index=False)
#     return dataList


# -------------------------------------------------------------------------------------
