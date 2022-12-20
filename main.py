import os
import io
import json
import uuid
import copy
from pprint import pprint

# import utils
from utils.utils import convert_time_to_str

# schemas (pydantic models)
from schemas import InvoiceWKMasterModel, InvoiceWKDetailModel

# database
from database.database import get_db_session
from database.models import (
    InvoiceWKMasterDBModel,
    InvoiceWKDetailDBModel,
    InvoiceMasterDBModel,
    InvoiceDetailDBModel,
)

# crud
from crud import create_invoice_wk_master

# pydantic and orm converters
from utils.orm_pydantic_convert import orm_to_pydantic, pydantic_to_orm

from fastapi.responses import Response
from datetime import timedelta, datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, Depends, Request, HTTPException

# ------------------ import lib and func (not required now) ------------------
# from auth import *
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordRequestForm
# from models import User, UserInDB, Token, TokenData, ConsumptionModel, SaveModel
# ----------------------------------------------------------------------------

app = FastAPI()

ROOT_URL = "/api/v1"


@app.post(f"{ROOT_URL}/InvoiceWorkManage/InvoiceWKMaster")
async def generate_invoice_work_manage_for_invoice_wk_master(
    request: Request, response: Response, invoice_wk_master_data: InvoiceWKMasterModel
):

    # convert invoice_wk_master_data to orm model
    invoice_wk_master_data = pydantic_to_orm(
        invoice_wk_master_data, InvoiceWKMasterDBModel
    )
    pprint(invoice_wk_master_data)

    # save invoice_wk_master_data to database
    db = next(get_db_session())
    create_invoice_wk_master(db, invoice_wk_master_data)
    return {"message": "invoice_work_manage_for_invoice_wk_master function works"}


@app.get(f"{ROOT_URL}/InvoiceWorkManage/InvoiceWKMaster")
async def get_invoice_work_manage_for_invoice_wk_master(
    request: Request, response: Response
):
    db = next(get_db_session())
    data = db.query(InvoiceWKMasterDBModel).all()
    # convert data to pydantic model
    data = [orm_to_pydantic(item, InvoiceWKMasterModel) for item in data]
    return data


@app.post(f"{ROOT_URL}/InvoiceWorkManage/InvoiceWKDetail")
async def generate_invoice_work_manage_for_invoice_wk_detail(
    request: Request, response: Response, invoice_wk_detail_data: InvoiceWKDetailModel
):
    try:
        pprint(invoice_wk_detail_data)
        print(type(invoice_wk_detail_data))
    except Exception as e:
        print(e)

    return {"message": "invoice_work_manage_for_invoice_wk_detail function works"}
