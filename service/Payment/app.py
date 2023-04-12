from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse

from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *

import os
from copy import deepcopy
from docxtpl import DocxTemplate, InlineImage


router = APIRouter()


# ------------------------------- 付款功能 -------------------------------
@router.get("/payment/datastream")
async def getPaymentDatastream(
    request: Request,
    db: Session = Depends(get_db),
):
    crudInvoiceWKMaster = CRUD(db, InvoiceWKMasterDBModel)
    crudInvoiceWKDetail = CRUD(db, InvoiceWKDetailDBModel)
    crudInvoiceMaster = CRUD(db, InvoiceMasterDBModel)
    crudInvoiceDetail = CRUD(db, InvoiceDetailDBModel)
    crudBillMaster = CRUD(db, BillMasterDBModel)
    crudBillDetail = CRUD(db, BillDetailDBModel)

    InvoiceWKMasterDataList = crudInvoiceWKMaster.get_with_condition(
        {"Status": "PAYING"}
    )


@router.post("/InvoiceWKMaster/payment")
async def paymentForInvWKMaster(
    request: Request,
    db: Session = Depends(get_db),
):
    pass
