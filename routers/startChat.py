import asyncio
import random
import time
from typing import Union
import uuid
from fastapi import APIRouter
# from fastapi.logger import logger
from pydantic import BaseModel

from models import ResponseModel
from utils import create_redis_client, create_response, logger

router = APIRouter()



class Req(BaseModel):
    user_id: str


class Resp(BaseModel):
    user_id: str
    room_id: str
    is_chat_beginer: bool  # 第一条消息


@router.post("", response_model=ResponseModel)
async def handler(req: Req):

    # TODO: 不能匹配自己

    rdc = create_redis_client()
    random.seed(int(time.time() *10**6))

    # 生成 1～100的随机数，来模拟匹配概率
    chat_with_human = True
    if random.randint(1, 100) <= 5:
        chat_with_human = True

    # 匹配算法参考 https://blog.csdn.net/qq_38403590/article/details/118420483

    # 要确保匹配双方的最后的room_id是一样的
    room_id = "" #
    room_users = []
    if not chat_with_human:
        # 为该用户匹配AI
        room_users = [req.user_id, "bot0001"]
        pass
    else:
        # 为该用户匹配人类
        active_user_id = rdc.lpop("matchlist")
        if active_user_id is not None:  # 有用户等待, 直接匹配
            rdc.hset("matchhash", active_user_id, req.user_id)

            # 返回匹配id号
            room_users = [active_user_id, req.user_id]

            room_id = rdc.hget("matchroomids", active_user_id)
        else:  # 没有等待用户, 自己加入等待
            rdc.hset("matchhash", req.user_id, "null")
            rdc.rpush("matchlist", req.user_id)
            rdc.hset("matchroomids", req.user_id , str(uuid.uuid4()))

            # 开始等待匹配 15s
            match_timeout = True
            for i in range(0, 5):
                await asyncio.sleep(1)
                other_user_id = rdc.hget("matchhash", req.user_id)
                if other_user_id != "null":
                    # 匹配成功
                    room_id = rdc.hget("matchroomids", req.user_id)
                    room_users = [req.user_id, other_user_id]
                    match_timeout = False
                    pass

            if match_timeout:
                # 匹配超时, 删除待匹配信息
                rdc.lrem("matchlist", 0, req.user_id)
                rdc.hdel("matchhash", req.user_id)
                rdc.hdel("matchroomids", req.user_id)
                room_id = ""
                return create_response(code=111, msg="match timeout, please try again")

    assert len(room_users) == 2, "invalid room users"
    # log.info('聊天室成员:{}'.format(room_users))


    # 将自己添加到聊天成员
    rdc.rpush("chatroommembers:" + room_id, req.user_id)

    # 决定谁先说话, 抢互斥锁
    is_chat_beginer = False
    await asyncio.sleep(random.randint(1, 50) / 1000)
    if 1 == rdc.hsetnx("chatturnmutex", room_id, req.user_id):
        is_chat_beginer = True

    # 设置游戏结束时间
    expire_time = int(time.time()) + 2*60
    rdc.set("chatroomexpire:"+ room_id, expire_time)

    rsp = create_response(
        data=Resp(
            user_id=req.user_id, room_id=room_id, is_chat_beginer=is_chat_beginer
        ),
    )

    return rsp
