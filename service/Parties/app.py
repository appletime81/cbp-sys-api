from fastapi import APIRouter, Request, status, Depends, Body
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import orm_to_pydantic
from copy import deepcopy

router = APIRouter()


# ------------------------------ Parties ------------------------------
# 查詢Parties
@router.get("/Parties/{PartiesCondition}")
async def getParties(
    request: Request,
    PartiesCondition: str,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, PartiesDBModel)
    if PartiesCondition == "all":
        PartiesDataList = crud.get_all()
    return PartiesDataList


@router.post("/Parties", status_code=status.HTTP_201_CREATED)
async def addParties(
    request: Request,
    PartiesPydanticData: PartiesSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, PartiesDBModel)
    crud.create(PartiesPydanticData)
    return {"message": "Party successfully created"}


# ---------------------------------------------------------------------
