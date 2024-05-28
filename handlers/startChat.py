import asyncio
import random
import time
from typing import Union
import uuid
from fastapi import APIRouter

# from fastapi.logger import logger
from pydantic import BaseModel

from models.models import ResponseModel
from utils.utils import create_redis_client, create_response, logger

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
    if rdc.hget("matchroomids", req.user_id) is not None:
        logger.error("用户 %s 已经在匹配中, 不能重复匹配 ", req.user_id)
        return create_response(code=1001, msg="already in queue")

    # 生成 1～100的随机数，来模拟匹配概率
    chat_with_human = False
    if random.randint(1, 100) <= 10:
        chat_with_human = True
        logger.info("用户%s, 匹配人类", req.user_id)
        # 如果 没人排队
        # ml = rdc.lrange("matchlist")
        # if ml is None or len(ml) == 0:
            # chat_with_human = False

    # 匹配算法参考 https://blog.csdn.net/qq_38403590/article/details/118420483

    # 要确保匹配双方的最后的room_id是一样的
    room_id = ""  #
    room_users = []
    if not chat_with_human:
        # 为该用户匹配AI
        room_users = [req.user_id, "bot0001"]
        room_id = str(uuid.uuid4())
        rdc.rpush("chatroommembers:" + room_id, *room_users)
        pass
    else:
        # 为该用户匹配人类
        active_user_id = rdc.lpop("matchlist")
        if active_user_id is not None and active_user_id == req.user_id:
            active_user_id

        if active_user_id is not None:  # 有用户等待, 直接匹配

            rdc.hset("matchhash", active_user_id, req.user_id)

            # 返回匹配id号
            room_users = [active_user_id, req.user_id]

            room_id = rdc.hget("matchroomids", active_user_id)
            # 将自己添加到聊天成员
            rdc.rpush("chatroommembers:" + room_id, *[active_user_id, req.user_id])

        else:  # 没有等待用户, 自己加入等待
            rdc.hset("matchhash", req.user_id, "null")
            rdc.rpush("matchlist", req.user_id)
            rdc.hset("matchroomids", req.user_id, str(uuid.uuid4()))

            # 开始等待匹配 15s
            match_timeout = True
            for i in range(0, 15):
                logger.info("用户{}正在排队匹配中...".format(req.user_id))
                await asyncio.sleep(1)
                other_user_id = rdc.hget("matchhash", req.user_id)
                if other_user_id != "null":
                    # 匹配成功
                    room_id = rdc.hget("matchroomids", req.user_id)
                    room_users = [req.user_id, other_user_id]
                    match_timeout = False
                    pass

            if match_timeout:
                logger.info("用户{}排队匹配超时".format(req.user_id))
                # 匹配超时, 删除待匹配信息
                room_id = ""
                rdc.hdel("matchhash", req.user_id)
                rdc.hdel("matchroomids", req.user_id)
                rdc.lrem("matchlist", 0, req.user_id)
                return create_response(code=111, msg="match timeout, please try again")

        if len(room_users) != 2:
            logger.error('聊天室成员数不为2:{}'.format(room_users))
            raise Exception("invalid room users")

    if room_id == '':
        logger.error("房间号为空")
        return create_response(code=1003, msg="system error, please try again later")
    logger.info("房间号: {}".format(room_id))
    logger.info("房间用户:{}".format(room_users))


    # 抢第一发言权
    is_chat_beginner = False
    rdc.hsetnx("chatturnmutex", room_id, random.choices(room_users)[0])

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
