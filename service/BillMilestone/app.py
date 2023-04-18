from fastapi import APIRouter, Request, status, Depends, Body
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy

router = APIRouter()


# ------------------------------ BillMilestone ------------------------------
# 查詢BillMilestone
@router.get("/BillMilestone/{BillMilestoneCondition}")
async def getBillMilestone(
    request: Request,
    BillMilestoneCondition: str,
    db: Session = Depends(get_db),
):
    """
    BillMilestoneCondition: str
    Example: "SubmarineCable={SubmarineCableName}&WorkTitle={WorkTitleName}"
    """

    BillMilestoneDictCondition = convert_url_condition_to_dict_ignore_date(
        BillMilestoneCondition
    )
    pprint(BillMilestoneDictCondition)
    if "End" in BillMilestoneDictCondition:
        end_condition = BillMilestoneDictCondition.pop("End")

    crudLiability = CRUD(db, LiabilityDBModel)
    LiabilityDataList = crudLiability.get_with_condition(BillMilestoneDictCondition)
    LiabilityDataList = [LiabilityData for LiabilityData in LiabilityDataList]
    if end_condition:
        LiabilityDictDataList = [
            orm_to_dict(LiabilityData)
            for LiabilityData in LiabilityDataList
            if LiabilityData.EndDate
        ]

    BillMilestoneDictDataList = list(
        set(
            [
                LiabilityDictData["BillMilestone"]
                for LiabilityDictData in LiabilityDictDataList
            ]
        )
    )

    return BillMilestoneDictDataList


# ---------------------------------------------------------------------------
