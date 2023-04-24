from fastapi import APIRouter, Request, status, Depends
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy

router = APIRouter()


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    crud = CRUD(db, UsersDBModel)
    body = await request.json()
    username = body["username"]
    password = body["password"]
    user = crud.get_with_condition({"username": username})
    if user:
        if user[0].password == password:
            return {"status": "true", "data": user[0]}
        else:
            return {"status": "false", "message": "密碼錯誤"}
    else:
        return {"status": "false", "message": "查無此帳號"}
