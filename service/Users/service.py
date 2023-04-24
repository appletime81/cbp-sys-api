from fastapi import APIRouter, Request, status, Depends
from crud import *
from get_db import get_db
from sqlalchemy.orm import Session
from utils.utils import *
from utils.orm_pydantic_convert import *
from copy import deepcopy
import configparser

router = APIRouter()


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    """
    {"username": xxx}
    """
    crud = CRUD(db, UsersDBModel)
    error_message = {"status": "false", "message": "error username or password"}

    config = configparser.ConfigParser()
    config.read("userinfo.ini")

    userInfo = await request.json()
    username = userInfo.get("username")
    inputPassword = userInfo.get("password")

    correctPassword = config[f"{username}"]["password"]

    userData = crud.get_with_condition({"UserID": username})
    if userData:
        if inputPassword == correctPassword:
            return {"status": "true", "user": userData.UserID}
        else:
            return error_message
    else:
        return error_message
