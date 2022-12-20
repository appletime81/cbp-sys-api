import os
import io
import json
import uuid
import copy

# model
from models import InvoiceWKMasterModel

from fastapi.responses import Response
from datetime import timedelta, datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status, Depends, Request, HTTPException

# ------------------ import lib and func (not required now) ------------------
# from auth import *
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordRequestForm
# from models import User, UserInDB, Token, TokenData, ConsumptionModel, SaveModel
# ----------------------------------------------------------------------------

app = FastAPI()


ROOT_URL = "/api/v1"


@app.post(f"{ROOT_URL}/InvoiceWorkManage")
async def invoice_work_manage(request: Request, response: Response):

    return {"message": "伺服器正常運作中"}
