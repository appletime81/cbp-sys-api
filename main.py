import os
import io
import json
import uuid
import copy
from pprint import pprint

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
from fastapi import FastAPI, status, Depends, Request, HTTPException

app = FastAPI()

ROOT_URL = "/api/v1"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------ InvoiceWKMaster ------------------------------
@app.post(f"{ROOT_URL}/InvoiceWorkManage/InvoiceWKMaster")
async def generate_invoice_work_manage_for_invoice_wk_master(
    request: Request,
    response: Response,
    invoice_wk_master_data: InvoiceWKMasterModel,
    db: Session = Depends(get_db),
):

    # convert invoice_wk_master_data to orm model
    invoice_wk_master_data = pydantic_to_orm(
        invoice_wk_master_data, InvoiceWKMasterDBModel
    )
    pprint(invoice_wk_master_data)

    # save invoice_wk_master_data to database
    create_invoice_wk_master(db, invoice_wk_master_data)
    return {"message": "invoice_work_manage_for_invoice_wk_master function works"}


@app.get(f"{ROOT_URL}/InvoiceWorkManage/InvoiceWKMaster")
async def get_invoice_work_manage_for_invoice_wk_master(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    data = get_all_invoice_wk_master(db)
    # convert data to pydantic model
    data = [orm_to_pydantic(item, InvoiceWKMasterModel) for item in data]
    return data


# -----------------------------------------------------------------------------

# ------------------------------ InvoiceWKDetail ------------------------------
@app.post(f"{ROOT_URL}/InvoiceWorkManage/InvoiceWKDetail")
async def generate_invoice_work_manage_for_invoice_wk_detail(
    request: Request,
    response: Response,
    invoice_wk_detail_data: InvoiceWKDetailModel,
    db: Session = Depends(get_db),
):

    # convert invoice_wk_detail_data to orm model
    invoice_wk_detail_data = pydantic_to_orm(
        invoice_wk_detail_data, InvoiceWKDetailDBModel
    )

    # save invoice_wk_detail_data to database
    create_invoice_wk_detail(db, invoice_wk_detail_data)

    return {"message": "invoice_work_manage_for_invoice_wk_detail function works"}


@app.get(f"{ROOT_URL}/InvoiceWorkManage/InvoiceWKDetail")
async def generate_invoice_work_manage_for_invoice_wk_detail(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    data = get_all_invoice_wk_detail(db)
    # convert data to pydantic model
    data = [orm_to_pydantic(item, InvoiceWKDetailModel) for item in data]
    return data


# -----------------------------------------------------------------------------
