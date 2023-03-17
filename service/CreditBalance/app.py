import os

from fastapi import APIRouter, Request, status, Depends
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/CreditBalance/{urlCondition}", status_code=status.HTTP_200_OK)
async def getCreditBalance(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, CreditBalanceDBModel)
    table_name = "CB"
    if "getByBillDetail=yes" not in urlCondition:
        if urlCondition == "all":
            CreditBalanceDataList = crud.get_all()
        elif "start" in urlCondition or "end" in urlCondition:
            dictCondition = convert_url_condition_to_dict(urlCondition)
            sql_condition = convert_dict_to_sql_condition(dictCondition, table_name)

            # get all CreditBalance by sql
            CreditBalanceDataList = crud.get_all_by_sql(sql_condition)
        else:
            dictCondition = convert_url_condition_to_dict(urlCondition)
            CreditBalanceDataList = crud.get_with_condition(dictCondition)
    else:
        # urlCondition: SubmarineCable=str&WorkTitle=str&BillMilestone=str&PartyName=str
        urlCondition = urlCondition.replace("getByBillDetail=yes", "")
        dictCondition = convert_url_condition_to_dict(urlCondition)
        CreditBalanceDataList = crud.get_with_condition(dictCondition)
    return CreditBalanceDataList


@router.post("/CreditBalanceStatement", status_code=status.HTTP_200_OK)
async def getCreditBalanceStatement(
    request: Request,
    urlCondition: str,
    db: Session = Depends(get_db),
):
    """
    {"CBID": int}
    """
    crud = CRUD(db, CreditBalanceStatementDBModel)
    CBID = (await request.json())["CBID"]
    CBStatementDataList = crud.get_with_condition({"CBID": CBID})
    return CBStatementDataList


@router.post("/CreditBalanceStatement/GenerateReport", status_code=status.HTTP_200_OK)
async def getCreditBalanceStatement(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    {"CBID": int}
    """

    crudCreditBalanceStatement = CRUD(db, CreditBalanceStatementDBModel)
    crudCreditBalance = CRUD(db, CreditBalanceDBModel)

    CBID = (await request.json())["CBID"]
    CBStatementDataList = crudCreditBalanceStatement.get_with_condition({"CBID": CBID})
    CBData = crudCreditBalance.get_with_condition({"CBID": CBID})[0]

    # use openpyxl to generate report

    workbook = Workbook()

    # generate col title
    worksheet = workbook.active
    worksheet.title = "CB歷程"
    worksheet.append(["BM", "Ref No.", "Description", "Debit", "Credit", "Balance"])
    OriginalCreditBalance = CBData.CurrAmount

    for tempCBStatementData in CBStatementDataList[::-1]:
        OriginalCreditBalance -= tempCBStatementData.TransAmount

    # generate dict 1-7 mapping to alphabet A-G
    alphabetDict = {}
    for i in range(1, 8):
        alphabetDict[i] = chr(i + 64)

    for i, CBStatementData in enumerate(CBStatementDataList):
        for j in range(1, 8):
            worksheet[f"{alphabetDict[j]}{i + 2}"].font = Font(bold=True)
            worksheet[f"{alphabetDict[j]}{i + 2}"].alignment = Alignment(
                horizontal="center", vertical="center"
            )
            worksheet[f"{alphabetDict[j]}{i + 2}"].border = Border(
                left=Side(border_style="thin", color="FF000000"),
                right=Side(border_style="thin", color="FF000000"),
                top=Side(border_style="thin", color="FF000000"),
                bottom=Side(border_style="thin", color="FF000000"),
            )
            # set width
            worksheet.column_dimensions[alphabetDict[j]].width = 20
        if i == 0:
            # add data and set style
            worksheet.append(
                [
                    CBData.BillMilestone,
                    CBStatementData.BillingNo,
                    CBData.Note,
                    "",
                    OriginalCreditBalance,
                    OriginalCreditBalance,
                ]
            )
            # SET STYLE
            worksheet[f"{alphabetDict[5]}{i+2}"].number_format = "#,##0.00"
            worksheet[f"{alphabetDict[5]}{i+2}"].fill = PatternFill(
                start_color="0000b0f0",
                end_color="00b0f0",
                fill_type="solid",
            )
        else:
            if CBStatementData.TransAmount > 0:
                worksheet.append(
                    [
                        CBData.BillMilestone,
                        CBStatementData.BillingNo,
                        CBData.Note,
                        CBStatementData.TransAmount,
                        "",
                        CBStatementData.OrgAmount + CBStatementData.TransAmount,
                    ]
                )
                worksheet[f"{alphabetDict[5]}{i + 2}"].number_format = "#,##0.00"
                worksheet[f"{alphabetDict[5]}{i + 2}"].fill = PatternFill(
                    start_color="0000b0f0",
                    end_color="00b0f0",
                    fill_type="solid",
                )
            else:
                worksheet.append(
                    [
                        CBData.BillMilestone,
                        CBStatementData.BillingNo,
                        CBData.Note,
                        "",
                        abs(CBStatementData.TransAmount),
                        CBStatementData.OrgAmount + CBStatementData.TransAmount,
                    ]
                )
                worksheet[f"{alphabetDict[5]}{i + 2}"].number_format = "#,##0.00"
                # 設定字體顏色
                worksheet[f"{alphabetDict[5]}{i + 2}"].font = Font(color="FF0000")

    # save file
    workbook.save("CB歷程.xlsx")

    # Streaming response
    file_name = "CB歷程.xlsx"
    return FileResponse(
        os.getcwd(),
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.post("/CreditBalance", status_code=status.HTTP_201_CREATED)
async def addCreditBalance(
    request: Request,
    CreditBalancePydanticData: CreditBalanceSchema,
    db: Session = Depends(get_db),
):
    crud = CRUD(db, CreditBalanceDBModel)
    CreditBalanceDictData = CreditBalancePydanticData.dict()
    CreditBalanceDictData["CreateDate"] = convert_time_to_str(datetime.now())
    CreditBalancePydanticData = CreditBalanceSchema(**CreditBalanceDictData)
    CreditBalanceData = crud.create(CreditBalancePydanticData)
    return {
        "message": "CreditBalance successfully created",
        "CreditBalance": CreditBalanceData,
    }


@router.post("/updateCreditBalance", status_code=status.HTTP_200_OK)
async def updateCreditBalance(
    request: Request,
    db: Session = Depends(get_db),
):
    CBDictData = await request.json()
    crud = CRUD(db, CreditBalanceDBModel)
    CBData = crud.get_with_condition({"CBID": CBDictData["CBID"]})[0]
    newCBData = crud.update(CBData, CBDictData)
    return {"message": "CreditBalance successfully updated", "newCBData": newCBData}
