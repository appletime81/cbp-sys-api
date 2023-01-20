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
from utils.orm_pydantic_convert import orm_to_pydantic
from utils.utils import *

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


@app.get(ROOT_URL + "/getInvoiceWKMaster&InvoiceWKDetail/{urlCondition}")
async def searchInvoiceWKMaster(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    getResult = []

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
            if (
                InvoiceWKMasterDictData["Status"] == "TEMPORARY"
                or InvoiceWKMasterDictData["Status"] == "VALIDATED"
            ):
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
        getResult.append(
            {
                "InvoiceWKMaster": InvoiceWKMasterDictData,
                "InvoiceWKDetail": InvoiceWKDetailDictDataList,
            }
        )
    pprint(getResult)
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

    return {"message": "success add InvoiceMaster and InvoiceDetail"}


# -------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------ Liability ------------------------------
@app.post(ROOT_URL + "/compareLiability")  # input data is "List[LiabilitySchema]"
async def compareLiability(request: Request, db: Session = Depends(get_db)):
    LiabilityDictDataList = await request.json()
    compareResultList = []
    crud = CRUD(db, LiabilityDBModel)
    for LiabilityDictData in LiabilityDictDataList:
        query_condition = {
            "SubmarineCable": LiabilityDictData["SubmarineCable"],
            "WorkTitle": LiabilityDictData["WorkTitle"],
            "BillMilestone": LiabilityDictData["BillMilestone"],
            "PartyName": LiabilityDictData["PartyName"],
        }
        LiabilityDataList = crud.get_with_condition(query_condition)
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
        LiabilityPydanticData = LiabilitySchema(**LiabilityDictData)
        crud.create(LiabilityPydanticData)
    return {"message": "success add Liability"}


# -----------------------------------------------------------------------
