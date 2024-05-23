import asyncio
import random
from typing import Union
from fastapi import APIRouter
from pydantic import BaseModel

from models import ResponseModel
from utils import create_redis_client, create_response

router = APIRouter()


class Req(BaseModel):
    user_id: str


class Resp(BaseModel):
    user_id: str
    room_id: str
    is_chat_beginer: bool  # 第一条消息


@router.post("", response_model=ResponseModel)
async def handler(req: Req):

    rdc = create_redis_client()

    # 生成 1～100的随机数，来模拟匹配概率
    chat_with_human = True
    if random.randint(1, 100) <= 5:
        chat_with_human = True

    # 匹配算法参考 https://blog.csdn.net/qq_38403590/article/details/118420483
    room_id = ""
    if chat_with_human:
        # 为该用户匹配人类
        active_user_id = rdc.lpop("matchlist")
        if active_user_id is not None:  # 有用户等待, 直接匹配
            rdc.hset("matchhash", active_user_id, req.user_id)

            # 返回匹配id号
            room_id = active_user_id + "vs" + req.user_id
            # TODO: room_id进行处理
            pass
        else:  # 没有等待用户, 自己加入等待
            rdc.hset("matchhash", req.user_id, "null")
            rdc.rpush("matchlist", req.user_id)

            # 开始等待匹配 15s
            match_timeout = True
            for i in range(0, 5):
                await asyncio.sleep(1)
                other_user_id = rdc.hget("matchhash", req.user_id)
                if other_user_id != "null":
                    # 匹配成功
                    # 返回匹配成功的id号
                    room_id = req.user_id + "vs" + other_user_id
                    match_timeout = False
                    # TODO: room_id进行处理
                    pass

            if match_timeout:
                # 匹配超时, 删除待匹配信息
                rdc.lrem("matchlist", 0, req.user_id)
                rdc.hdel("matchhash", req.user_id)
                room_id = ""
                return create_response(code=111, msg="match timeout, please try again")
            pass
    else:
        # 为该用户匹配AI
        room_id = req.user_id + "vs" + "bot0001"
        pass

    # 决定谁先说话
    is_chat_beginer = False
    if room_id.startswith(req.user_id):
        is_chat_beginer = True

    rsp = create_response(
        data=Resp(
            user_id=req.user_id, room_id=room_id, is_chat_beginer=is_chat_beginer
        ),
    )

    # 创建房间
    # id = rdc.incr('roomcounter')
    # rdc.set(  'chatroom:' + room_id + str(id) , room_id)
    rdc.set("chatroom:" + room_id, room_id)
    return rsp
