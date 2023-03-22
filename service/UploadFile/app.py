import os
import shutil

from fastapi import APIRouter, Request, status, Depends, File, UploadFile
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy

router = APIRouter()


# ------------------------------ Upload file ------------------------------


@router.post("/uploadfile")
async def uploadfile(
    request: Request, db: Session = Depends(get_db), file: UploadFile = File(...)
):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": file.filename}


@router.post("/UploadSignedBillMaster/{urlCondition}")
async def uploadSignedBillMaster(
    request: Request, db: Session = Depends(get_db), file: UploadFile = File(...)
):
    """
    urlCondition: BillMasterID = int
    """
    # TODO: Update BillMaster URI
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)



    # os.system(f"aws s3 cp {file.filename} s3://cht-deploy-bucket-1/{file.filename}")
    # # get URI
    # URI = os.system(f"aws s3 presign s3://cht-deploy-bucket-1/{file.filename}")
    # print(URI)
    return {"file_name": file.filename}


# -------------------------------------------------------------------------
