from fastapi import APIRouter
from pydantic import BaseModel

from models import ResponseModel
from utils import create_redis_client, create_response

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

    users = rdc.get('chatroom:' + req.room_id)
    if users is None:
        #TODO
        pass


    user_ids = str(users).split('vs')
    assert len(user_ids) == 2, "invalid room"

    opponent_user_id = user_ids[0] if req.user_id != user_ids[0] else user_ids[1]

    opponent_role = 'bot' if opponent_user_id.startswith('bot') else 'human'
    rsp = Resp(user_id=req.user_id, room_id=req.room_id, is_win=False, rewards=0)
    guess_role = 'human' if req.human else 'bot'
    if guess_role == opponent_role:
        rsp.is_win = True
        rsp.rewards = 100


    # TODO: 更新聊天室的状态为结束

    return create_response(data=rsp)
