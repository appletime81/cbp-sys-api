from fastapi import APIRouter, Request, status, Depends
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import orm_to_pydantic
from copy import deepcopy

router = APIRouter()

@router.post("/CreditBalance", status_code=status.HTTP_201_CREATED)
async def addCreditBalance(
    request: Request,
    CreditBalancePydanticData: CreditBalanceSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, CreditBalanceDBModel)
    crud.create(CreditBalancePydanticData)
    return {
        "message": "CreditBalance successfully created",
    }