from fastapi import FastAPI

from routers import startChat, sendChatMsg, queryChat, finishChat

app = FastAPI()


app.include_router(startChat.router, prefix="/startChat", tags=["startChat"])
app.include_router(sendChatMsg.router, prefix="/sendChatMsg", tags=["sendChatMsg"])
app.include_router(queryChat.router, prefix="/queryChat", tags=["queryChat"])
app.include_router(finishChat.router, prefix="/finishChat", tags=["finishChat"])
