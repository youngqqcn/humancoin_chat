from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Req(BaseModel):
    user_id: str
    room_id: str
    msg: str


class Resp(BaseModel):
    user_id: str
    room_id: str
    msg_id: str


@router.post("", response_model=Resp)
async def handler(req: Req):
    rsp = Resp(user_id=req.user_id, room_id=req.user_id, msg_id='msg_id_xxx')
    return rsp
