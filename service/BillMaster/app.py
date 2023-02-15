from fastapi import APIRouter, Request, status, Depends, Body
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy

router = APIRouter()


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
    BillingNo = request_data["BillingNo"]

    crud = CRUD(db, BillMasterDBModel)
    BillMasterData = crud.get_with_condition({"BillingNo": BillingNo})

    if BillMasterData:
        return {"isExist": True}
    else:
        return {"isExist": False}
