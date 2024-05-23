import json
import time
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models import ResponseModel
from utils import create_redis_client, create_response

router = APIRouter()


class Req(BaseModel):
    user_id: str
    room_id: str
    msg: str


class Resp(BaseModel):
    user_id: str
    room_id: str
    msg_id: str


@router.post("", response_model=ResponseModel)
async def handler(req: Req):

    rdc = create_redis_client()
    # 检查房间是否存在
    # TODO:是否过期,  在value中增加过期时间
    if not rdc.exists("chatroom:" + req.room_id):
        raise HTTPException(status_code=404, detail="room not found")

    # TODO: 检查当前是否是该用户发言,
    # 判断最后一条消息是否是

    ts = int(time.time() * 1000)
    msg_id = str(uuid.uuid4())
    msg = {
        "user_id": req.user_id,
        "content": req.msg,
        "timestamp": ts,
        "msg_id": msg_id,
    }
    rdc.zadd("chatchannel:" + req.room_id, {json.dumps(msg): ts})

    rsp = Resp(user_id=req.user_id, room_id=req.room_id, msg_id=msg_id)
    return create_response(data=rsp)
