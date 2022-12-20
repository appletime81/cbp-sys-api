import os
import io
import json
import uuid
import copy
from pprint import pprint

# import utils
from utils.utils import convert_time_to_str

# model
from models import InvoiceWKMasterModel, InvoiceWKDetailModel

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
    # check type
    if not isinstance(invoice_wk_master_data, InvoiceWKMasterModel):
        return {"status": "error", "message": "invoice_wk_master_data is not InvoiceWKMasterModel type"}
    invoice_wk_master_data_dict = invoice_wk_master_data.dict()
    invoice_wk_master_data_dict["IssueDate"] = invoice_wk_master_data_dict[
        "IssueDate"
    ].astimezone()
    invoice_wk_master_data_dict["IssueDate"] = convert_time_to_str(
        invoice_wk_master_data_dict["IssueDate"]
    )

    invoice_wk_master_data_dict["InvoiceDueDate"] = invoice_wk_master_data_dict[
        "InvoiceDueDate"
    ].astimezone()
    invoice_wk_master_data_dict["InvoiceDueDate"] = convert_time_to_str(
        invoice_wk_master_data_dict["InvoiceDueDate"]
    )

    # print datetime time zone info
    print(
        invoice_wk_master_data_dict["IssueDate"],
        type(invoice_wk_master_data_dict["IssueDate"]),
    )
    print(
        invoice_wk_master_data_dict["InvoiceDueDate"],
        type(invoice_wk_master_data_dict["InvoiceDueDate"]),
    )
    return {"message": "invoice_work_manage_for_invoice_wk_master function works"}


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
