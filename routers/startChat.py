
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Req(BaseModel):
    user_id: str


class Resp(BaseModel):
    user_id: str
    room_id: str
    is_chat_beginer: bool  # 第一条消息


@router.post("", response_model=Resp)
async def handler(req: Req):
    rsp = Resp(user_id=req.user_id, room_id="xxxxx", is_chat_beginer=False)
    return rsp

