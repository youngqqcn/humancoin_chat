import json
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

from models import ResponseModel
from utils import create_redis_client, create_response


router = APIRouter()


class Req(BaseModel):
    user_id: str
    room_id: str


class Msg(BaseModel):
    msg_id: str
    content: str
    user_id: str
    timestamp: int


class Resp(BaseModel):
    user_id: str
    room_id: str
    msgs: List[Msg]


@router.post("", response_model=ResponseModel)
async def handler(req: Req):

    rdc = create_redis_client()

    # 查询消息记录
    msgs = rdc.zrange("chatchannel:" + req.room_id, 0, -1, desc=True)
    rsp_msgs = []
    if msgs is not None:
        for item in msgs:
            msg = json.loads(item)
            rsp_msgs.append(Msg(**msg))

    rsp = Resp(
        user_id=req.user_id,
        room_id=req.room_id,
        msgs=rsp_msgs,
    )
    return create_response(data=rsp)
