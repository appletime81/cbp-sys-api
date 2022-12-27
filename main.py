import os
import io
import json
import uuid
import copy
from pprint import pprint

import service

# import utils
from utils.utils import convert_time_to_str

# schemas (pydantic models)
from schemas import *

# database
from database.engine import *
from database.models import *

# crud
from crud import *

# pydantic and orm converters
from utils.orm_pydantic_convert import orm_to_pydantic, pydantic_to_orm

from fastapi.responses import Response
from datetime import timedelta, datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, Depends, Request, HTTPException, Body
from get_db import get_db

app = FastAPI()

ROOT_URL = "/api/v1"

app.include_router(
    service.router, prefix=ROOT_URL, tags=["service"]
)


# ------------------------------ InvoiceWKMaster and InvoiceWKDetail and InvoiceMaster and InvoiceDetail ------------------------------


@app.post(
    f"{ROOT_URL}/generateInvoiceWKMaster&InvoiceWKDetail&InvoiceMaster&InvoiceDetail"
)
async def generateInvoiceWKMasterInvoiceWKDetailInvoiceMasterInvoiceDetail(
        request: Request,
        invoice_data: dict = Body(...),
        db: Session = Depends(get_db),
):
    # ---------------- handle InvoiceWKMaster ----------------
    if not invoice_data["IsPro"]:
        # 建立發票工作主檔
        InvoiceWKMasterDictData = invoice_data["InvoiceWKMaster"]
        InvoiceWKMasterDictData["CreateDate"] = convert_time_to_str(datetime.now())
        InvoiceWKMasterPydanticData = InvoiceWKMasterSchema(**InvoiceWKMasterDictData)  # convert dict to pydantic model
        create_invoice_wk_master_response = await service.InvoiceWKMaster(
            request, InvoiceWKMasterPydanticData, db
        )
        # 建立發票工作明細檔
        WKMasterID = create_invoice_wk_master_response["WKMasterID"]


    if invoice_data["IsPro"]:
        pass



    return {"message": "success"}
