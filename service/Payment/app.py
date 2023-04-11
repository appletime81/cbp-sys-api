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
@router.post("/InvoiceWKMaster/payment")
async def paymentForInvWKMaster(
    request: Request,
    db: Session = Depends(get_db),
):
    pass
