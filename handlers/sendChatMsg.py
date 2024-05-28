import json
import time
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.models import ResponseModel
from utils.utils import create_redis_client, create_response, logger

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

    logger.info("请求参数: %s", req.json())

    rdc = create_redis_client()
    # 检查房间是否存在
    expire_time = rdc.get("chatroomexpire:" + req.room_id)
    if expire_time is None:
        logger.info(f"房间未找到:{req.room_id}")
        raise HTTPException(status_code=404, detail="room not found")

    # 检查房间是否过期, 过期了就不再插入redis，直接返回即可
    if int(expire_time) <= int(time.time()):
        logger.warning(f"房间:{req.room_id} 聊天已结束, 不能再发送消息")
        rsp = Resp(user_id=req.user_id, room_id=req.room_id, msg_id=str(uuid.uuid4()))
        return create_response(data=rsp)

    # 检查当前是否轮到该用户发言,
    user_id = rdc.hget("chatturnmutex", req.room_id)
    if user_id is None:
        user_id = "x"
    if user_id != req.user_id:
        logger.error(f'房间: {req.room_id}, 用户不是当前说话人: {req.user_id}, 说话人:{user_id}')
        raise HTTPException("1002", "not turn")

    # 将消息插入
    ts = int(time.time())
    msg_id = str(uuid.uuid4())
    msg = {
        "user_id": req.user_id,
        "content": req.msg,
        "timestamp": ts,
        "msg_id": msg_id,
    }
    rdc.zadd("chatchannel:" + req.room_id, {json.dumps(msg): ts})

    logger.info(f"房间:{req.room_id}, 用户:{req.user_id}, 发送消息: {req.msg}")

    # 获取该用户的对手
    room_members = rdc.lrange("chatroommembers:" + req.room_id, 0, -1)
    opponent_user_id =  room_members[0] if room_members[0] != req.user_id else room_members[1]

    # 切换当前发言人
    logger.info("切换房间{}的发言人为:{}".format(req.room_id, opponent_user_id))
    rdc.hset("chatturnmutex", req.room_id, opponent_user_id)

    if str(opponent_user_id).startswith('bot'):
        # 如果是用户的对手是AI, 则插入一条消息到队列, AI机器人消费, 并回复
        rdc.rpush("chataimsgqueue", req.room_id)
        logger.info("轮到AI发言, 发送消息队列成功")
        pass

    rsp = Resp(user_id=req.user_id, room_id=req.room_id, msg_id=msg_id)
    logger.info("响应内容:{}".format(rsp))
    return create_response(data=rsp)
