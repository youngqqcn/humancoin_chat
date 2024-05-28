import json
import time
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

from models.models import ResponseModel
from utils.utils import create_redis_client, create_response, logger



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
    remaining_sec: int
    msgs: List[Msg]


@router.post("", response_model=ResponseModel)
async def handler(req: Req):
    logger.info("请求参数: %s", req.json())

    rdc = create_redis_client()

    # 查询消息记录
    msgs = rdc.zrange("chatchannel:" + req.room_id, 0, -1, desc=True)
    logger.info("历史消息长度: {}".format(len(msgs)))
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
    elif int(expire_time) <= int(time.time()):
        time_up = True

    turn_user = rdc.hget("chatturnmutex", req.room_id)
    is_my_turn = True if turn_user is not None and turn_user == req.user_id else False
    remaining_sec = max(0,  int(expire_time) - int(time.time()))
    rsp = Resp(
        user_id=req.user_id,
        room_id=req.room_id,
        msgs=rsp_msgs,
        is_my_turn=is_my_turn,
        is_time_up=time_up,
        expire_time=expire_time,
        remaining_sec= remaining_sec
    )
    logger.info("响应内容:{}".format(rsp))
    return create_response(data=rsp)
