import json
import random
import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from utils import ResponseModel
from utils import HcError, create_redis_client, create_response, logger

# 积分奖励
win_rewards = 10
lose_rewards = -5

router = APIRouter()


class Req(BaseModel):
    user_id: str
    room_id: str
    human: bool


class Resp(BaseModel):
    user_id: str
    room_id: str
    is_win: bool
    rewards: float


@router.post("", response_model=ResponseModel)  # , response_class=JSONResponse)
async def handler(req: Req):
    random.seed(int(time.time() * 10**6))
    logger.info("请求参数: %s", req.json())
    rdc = create_redis_client()
    # 检查房间是否存在
    expire_time = rdc.get("chatroomexpire:" + req.room_id)
    if expire_time is None:
        logger.info(f"房间未找到:{req.room_id}")
        return create_response(code=HcError.ROOM_NOT_FOUND)

    # 只能判断一次, 防止重复判断
    result = rdc.hget("chatroomresult:" + req.room_id, req.user_id)
    if result is not None:
        logger.info("重复判断, room_id:{}, user_id:{}", req.room_id, req.user_id)
        rsp = Resp(user_id=req.user_id, room_id=req.room_id, is_win=False, rewards=0)
        if result == "win":
            rsp.is_win = True
            rsp.rewards = win_rewards
        return create_response(data=rsp)

    # 获取该用户的对手
    room_members = rdc.lrange("chatroommembers:" + req.room_id, 0, -1)
    assert len(room_members) == 2, "invalid room"

    opponent_user_id = (
        room_members[0] if room_members[0] != req.user_id else room_members[1]
    )
    # 判定胜负, 目前的规则允许双方都胜利， 而不是用户双方的博弈, 而是和系统博弈
    opponent_role = "bot" if opponent_user_id.startswith("bot") else "human"
    rsp = Resp(user_id=req.user_id, room_id=req.room_id, is_win=False, rewards=0)
    guess_role = "human" if req.human else "bot"
    if guess_role == opponent_role:
        rsp.is_win = True
        rsp.rewards = win_rewards
    else:
        rsp.is_win = False
        rsp.rewards = lose_rewards

    # 系统作弊
    if rsp.is_win and guess_role == "bot":
        # 10%的概率，由系统作弊取胜
        if random.randint(1, 100) < 10:
            rsp.is_win = False
            rsp.rewards = lose_rewards
            logger.info("系统作弊, 房间:{}, 用户:{}".format(req.room_id, req.user_id))

    # 更新聊天室的状态为结束
    rdc.hset(
        "chatroomresult:" + req.room_id, req.user_id, "win" if rsp.is_win else "lose"
    )

    # 更新胜率统计
    rdc.hincrby("chattotals", req.user_id)
    if rsp.is_win:
        rdc.hincrby("chatwins", req.user_id)

    # 发送消息，更新积分
    rdc.rpush(
        "chatpointqueue",
        json.dumps(
            {
                "user_id": req.user_id,
                "room_id": req.room_id,
                "points": rsp.rewards,
                "timestamp": int(time.time()),
            }
        ),
    )
    logger.info(
        "房间:{}, 用户:{}, 更新积分: {},  发送积分消息队列成功 ".format(
            req.room_id, req.user_id, rsp.rewards
        )
    )

    logger.info("响应内容:{}".format(rsp))
    return create_response(data=rsp)
