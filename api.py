from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from exceptions.exceptions import general_exception_handler, http_exception_handler
from handlers import startChat, sendChatMsg, queryChat, finishChat
from utils.jwt_middleware import verify_jwt
from utils.utils import create_response

app = FastAPI()

# 添加全局异常处理器


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    jwt_token = request.headers.get("Token")
    json_body = await request.json()
    user_id = json_body['user_id']
    if verify_jwt(jwtoken=jwt_token, user_id=user_id):
        return await call_next(request)

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=create_response(
            msg="invalid token", code=status.HTTP_401_UNAUTHORIZED
        ).dict(),
    )


app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(startChat.router, prefix="/startChat", tags=["startChat"])
app.include_router(sendChatMsg.router, prefix="/sendChatMsg", tags=["sendChatMsg"])
app.include_router(queryChat.router, prefix="/queryChat", tags=["queryChat"])
app.include_router(finishChat.router, prefix="/finishChat", tags=["finishChat"])
