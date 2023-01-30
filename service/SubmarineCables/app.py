from fastapi import APIRouter, Request, status, Depends, Body
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import orm_to_pydantic
from copy import deepcopy

router = APIRouter()

# ------------------------------ SubmarineCables ------------------------------
# 查詢SubmarineCables
@router.get("/SubmarineCables/{SubmarineCablesCondition}")
async def getSubmarineCables(
    request: Request,
    SubmarineCablesCondition: str,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, SubmarineCablesDBModel)
    if SubmarineCablesCondition == "all":
        SubmarineCablesDataList = crud.get_all()
    else:
        SubmarineCablesDictCondition = convert_url_condition_to_dict_ignore_date(
            SubmarineCablesCondition
        )
        SubmarineCablesDataList = crud.get_with_condition(SubmarineCablesDictCondition)

    return SubmarineCablesDataList


@router.post("/SubmarineCables", status_code=status.HTTP_201_CREATED)
async def addSubmarineCables(
    request: Request,
    SubmarineCablesPydanticData: SubmarineCablesSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, SubmarineCablesDBModel)
    crud.create(SubmarineCablesPydanticData)
    return {"message": "SubmarineCable successfully created"}


# -----------------------------------------------------------------------------
