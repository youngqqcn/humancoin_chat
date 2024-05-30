import os
from fastapi import FastAPI, HTTPException

from utils.exceptions import general_exception_handler, http_exception_handler
from handlers import startChat, sendChatMsg, queryChat, finishChat, getWinRate
from utils.hcjwt import jwt_middleware
from starlette.middleware.base import BaseHTTPMiddleware

os.environ["PYTHONUNBUFFERED"] = "1"

app = FastAPI()


app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(startChat.router, prefix="/startChat", tags=["startChat"])
app.include_router(sendChatMsg.router, prefix="/sendChatMsg", tags=["sendChatMsg"])
app.include_router(queryChat.router, prefix="/queryChat", tags=["queryChat"])
app.include_router(finishChat.router, prefix="/finishChat", tags=["finishChat"])
app.include_router(getWinRate.router, prefix="/getWinRate", tags=["getWinRate"])

if os.getenv('HCJWTENABLE') is not None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=jwt_middleware)
