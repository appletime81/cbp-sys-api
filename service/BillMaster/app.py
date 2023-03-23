from fastapi import APIRouter, Request, status, Depends, Body
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy

router = APIRouter()


# ------------------------------ BillMaster ------------------------------
@router.get("/BillMaster/{urlCondition}")
async def getBillMaster(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, BillMasterDBModel)
    if urlCondition == "all":
        BillMasterDataList = crud.get_all()
    else:
        dictCondition = convert_url_condition_to_dict(urlCondition)
        BillMasterDataList = crud.get_with_condition(dictCondition)

    return BillMasterDataList


@router.post("/generateBillingNo")
async def generateBillingNo(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    {
      "subBillingNo": "test",
      "IssueDate": "2021-01-01",
      "DueDate": "2021-01-02",
      "InvoiceMaster": [
        {
          "InvMasterID": 1
        },
        {
          "InvMasterID": 2
        },
        {
          "InvMasterID": 3
        }
      ]
    }
    """
    request_data = await request.json()
    InvMasterID = request_data["InvoiceMaster"][0]["InvMasterID"]
    subBillingNo = request_data["subBillingNo"]
    crud = CRUD(db, InvoiceMasterDBModel)
    InvoiceMasterData = crud.get_with_condition({"InvMasterID": InvMasterID})[0]
    SubmarineCable = InvoiceMasterData.SubmarineCable
    PartyName = InvoiceMasterData.PartyName

    # 如果使用者沒有填subBillingNo，則使用當前時間當作subBillingNo
    if not subBillingNo:
        subBillingNo = convert_time_to_str(datetime.now())
        subBillingNo = subBillingNo.replace("-", "").replace(":", "").replace(" ", "")

    BillingNo = f"{SubmarineCable}-CBP-{PartyName}-{subBillingNo}"

    return {"BillingNo": BillingNo}


@router.post("/checkBillingNo")
async def checkBillingNo(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    {
      "BillingNo": "test"
    }
    """
    request_data = await request.json()
    print("BillingNo: ", request_data["BillingNo"])
    BillingNo = request_data["BillingNo"]

    crud = CRUD(db, BillMasterDBModel)
    BillMasterData = crud.get_with_condition({"BillingNo": BillingNo})

    if BillMasterData:
        return {"isExist": True}
    else:
        return {"isExist": False}


@router.post("/checkBillingNo/convert")
async def checkBillingNoConvert(
    request: Request,
    db: Session = Depends(get_db),
):
    BillingNo = (await request.json())["BillingNo"]
    BillingNo = BillingNo.replace("-CBP-", "-")
    crudSubmarineCables = CRUD(db, SubmarineCablesDBModel)
    crudParties = CRUD(db, PartiesDBModel)
    SubmarineCablesDataList = crudSubmarineCables.get_all()
    PartiesDataList = crudParties.get_all()

    SubmarineCablesMapping = dict(
        [
            (SubmarineCablesData.CableName, SubmarineCablesData.CableCode)
            for SubmarineCablesData in SubmarineCablesDataList
        ]
    )
    WorkTitleMapping = {"Upgrade": "UP", "Construction": "CO", "O&M": "OM"}
    PartyNameMapping = dict(
        [(PartyData.PartyName, PartyData.PartyCode) for PartyData in PartiesDataList]
    )
    BillingNoStrList = BillingNo.split("-")
    newBillingNoList = []

    # {SubmarineCable}-{WorkTitle}-{PartyName}-{YYYYMMDDmm}
    for i, substring in enumerate(BillingNoStrList):
        if i == 0:
            newBillingNoList.append(SubmarineCablesMapping[substring])
        elif i == 1:
            newBillingNoList.append(WorkTitleMapping[substring])
        elif i == 2:
            newBillingNoList.append(PartyNameMapping[substring])
        else:
            newBillingNoList.append(substring)

    # {0}{1}-{2}{3}
    newBillingNo = f"{newBillingNoList[0]}{newBillingNoList[1]}-{newBillingNoList[2]}{newBillingNoList[3]}"
    return {"BillingNo": newBillingNo}
