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


@router.post("/uploadSignedBillMaster/{BillMasterID}")
async def uploadSignedBillMaster(
    request: Request,
    BillMasterID: str,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    """
    {
        "BillMasterID": int
    }
    """
    BillMasterID = int(BillMasterID)
    crudBillMaster = CRUD(db, BillMasterDBModel)
    BillMasterID = (await request.json())["BillMasterID"]
    BillMasterData = crudBillMaster.get_with_condition({"BillMasterID": BillMasterID})[
        0
    ]

    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    os.system(f"aws s3 cp {file.filename} s3://cht-deploy-bucket-1/{file.filename}")

    # get URI
    URI, _ = os.system(f"aws s3 presign s3://cht-deploy-bucket-1/{file.filename}")

    # update BillMaster
    newBillMasterData = deepcopy(BillMasterData)
    newBillMasterData.URI = URI

    newBillMasterData = crudBillMaster.update(
        BillMasterData, orm_to_dict(newBillMasterData)
    )
    return {"message": "success", "file_name": file.filename, "URI": URI}


# -------------------------------------------------------------------------
