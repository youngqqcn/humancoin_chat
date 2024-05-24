import json
import time
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

from models import ResponseModel
from utils import create_redis_client, create_response, create_logger

log = create_logger()


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
    is_my_turn: bool
    is_time_up: bool
    expire_time: int
    msgs: List[Msg]


@router.post("", response_model=ResponseModel)
async def handler(req: Req):

    rdc = create_redis_client()
    log.info("==============")

    # 查询消息记录
    msgs = rdc.zrange("chatchannel:" + req.room_id, 0, -1, desc=True)
    rsp_msgs = []
    if msgs is not None:
        for item in msgs:
            msg = json.loads(item)
            rsp_msgs.append(Msg(**msg))

    expire_time = rdc.get("chatroomexpire:" + req.room_id)
    time_up = False
    if expire_time is None:
        expire_time = 0  # int(time.time())
        time_up = True

    turn_user = rdc.hget("chatturnmutex", req.room_id)
    is_my_turn = True if turn_user is not None and turn_user == req.user_id else False
    rsp = Resp(
        user_id=req.user_id,
        room_id=req.room_id,
        msgs=rsp_msgs,
        is_my_turn=is_my_turn,
        is_time_up=time_up,
        expire_time=expire_time,
    )
    return create_response(data=rsp)
