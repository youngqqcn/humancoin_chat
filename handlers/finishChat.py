from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.models import ResponseModel
from utils.utils import create_redis_client, create_response

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


@router.post("", response_model=ResponseModel)
async def handler(req: Req):
    rdc = create_redis_client()

    # 检查房间是否存在
    expire_time = rdc.get("chatroomexpire:" + req.room_id)
    if expire_time is None:
        raise HTTPException(status_code=1001, detail="room not found")

    # 只能判断一次, 防止重复判断
    result = rdc.hget("chatroomresult:" + req.room_id, req.user_id)
    if result is not None:
        rsp = Resp(user_id=req.user_id, room_id=req.room_id, is_win=False, rewards=0)
        if result == "win":
            rsp.is_win = True
            rsp.rewards = 100
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
        rsp.rewards = 100

    # 更新聊天室的状态为结束
    rdc.hset(
        "chatroomresult:" + req.room_id, req.user_id, "win" if rsp.is_win else "lose"
    )

    # TODO: 发送消息，增加积分

    return create_response(data=rsp)
