import asyncio
import math
import random
import time
from typing import Union
import uuid
from fastapi import APIRouter

from pydantic import BaseModel

from utils import ResponseModel
from utils import HcError, create_redis_client, create_response, logger

def P(n, a=0.3, b=0.7, k=0.2):
    """
    主动匹配的概率函数，
    n是排队队列中的人数
    """
    return a + (b - a) * (1 - math.exp(-k * n))


router = APIRouter()


class Req(BaseModel):
    user_id: str


class Resp(BaseModel):
    user_id: str
    room_id: str
    is_chat_beginner: bool  # 第一条消息


@router.post("", response_model=ResponseModel)
async def handler(req: Req):

    logger.info("请求参数: %s", req.json())
    random.seed(int(time.time() * 10**6))
    rdc = create_redis_client()

    # 如果已经开始排队匹配，不能重复排队
    queue_users = rdc.lrange("matchlist", 0, -1)
    if queue_users is not None and len(queue_users) > 0:
        if req.user_id in set(queue_users):
            logger.error("用户 %s 已经在匹配队列中, 不能重复匹配 ", req.user_id)
            return create_response(code=HcError.ALREADY_QUEUE)

    # 开始匹配
    room_id = ""
    room_users = []
    match_ok = False
    if queue_users is not None and len(queue_users) > 0:
        # 计算主动匹配概率
        positive_match_possibility = P(len(queue_users), 0.4)
        # 是否主动匹配
        is_positive_match = (random.randint(1, 100) < positive_match_possibility*100)
        if is_positive_match:
            # 为该用户匹配人类
            active_user_id = rdc.lpop("matchlist")
            if active_user_id is not None:  # 有用户等待, 直接匹配
                if rdc.hget("matchhash", active_user_id) is not None:
                    rdc.hset("matchhash", active_user_id, req.user_id)
                    # 返回匹配id号
                    room_users = [active_user_id, req.user_id]
                    room_id = rdc.hget("matchroomids", active_user_id)
                    # 将自己添加到聊天成员
                    rdc.sadd("chatroommembers:" + room_id, *[active_user_id, req.user_id])
                    match_ok = True

    # 如果没有主动匹配成功, 都进入被动匹配
    if not match_ok:
        match_timeout = True
        rdc.hset("matchhash", req.user_id, "null")
        rdc.rpush("matchlist", req.user_id)
        rdc.hset("matchroomids", req.user_id, str(uuid.uuid4()))
        # 开始等待匹配 15s
        for i in range(0,   random.randint(10, 15) ):
            logger.info("用户{}正在排队匹配中...".format(req.user_id))
            await asyncio.sleep(1)
            other_user_id = rdc.hget("matchhash", req.user_id)
            if other_user_id != "null":
                # 匹配成功
                room_id = rdc.hget("matchroomids", req.user_id)
                room_users = [req.user_id, other_user_id]
                rdc.sadd("chatroommembers:" + room_id, *room_users)
                match_timeout = False
                break

        # 匹配超时, 删除待匹配信息
        if match_timeout:
            logger.info("用户{}排队匹配超时".format(req.user_id))
            room_id = ""
            rdc.lrem("matchlist", 0, req.user_id)
            rdc.hdel("matchhash", req.user_id)
            rdc.hdel("matchroomids", req.user_id)
        # 如果被动匹配超时，匹配AI, X%的概率匹配成功
        if match_timeout:
            is_match_ai = (random.randint(1, 100) <= 80)
            if is_match_ai:
                logger.info("用户%s, 匹配人类", req.user_id)
                # 为该用户匹配AI
                room_users = [req.user_id, "bot0001"]
                room_id = str(uuid.uuid4())
                rdc.sadd("chatroommembers:" + room_id, *room_users)
            else:
                logger.info("未匹配AI, 让用户重试...")
                return create_response(code=HcError.MATCH_TIMEOUT)
    # 匹配成功
    if len(room_users) != 2:
        logger.error("聊天室成员数不为2:{}".format(room_users))
        raise Exception("invalid room users")
    if room_id == "":
        logger.error("房间号为空")
        return create_response(code=HcError.SYSTEM_ERROR)
    logger.info("房间号: {}".format(room_id))
    logger.info("房间用户:{}".format(room_users))

    # 抢第一发言权
    random.seed(int(time.time() * 10**6 + 2983))
    random.shuffle(room_users)
    is_chat_beginner = False
    rdc.hsetnx("chatturnmutex", room_id, random.choices(room_users , k=1)[0])
    first_chat_user_id = rdc.hget("chatturnmutex", room_id)
    assert first_chat_user_id is not None, "invalid room"
    if first_chat_user_id == req.user_id:
        is_chat_beginner = True

    # 如果是AI开始发言，则需要发送消息通知AI
    if first_chat_user_id.startswith("bot"):
        rdc.rpush("chataimsgqueue", room_id)
        logger.info("AI先发言, 发送消息到消息队列成功")

    # 设置游戏结束时间
    expire_time = int(time.time()) + 2 * 60
    rdc.set("chatroomexpire:" + room_id, expire_time)

    rsp = create_response(
        data=Resp(
            user_id=req.user_id, room_id=room_id, is_chat_beginner=is_chat_beginner
        ),
    )
    logger.info("响应内容:{}".format(rsp))
    return rsp
