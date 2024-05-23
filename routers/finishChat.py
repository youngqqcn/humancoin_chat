from fastapi import APIRouter
from pydantic import BaseModel

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


@router.post("", response_model=Resp)
async def handler(req: Req):
    rsp = Resp(user_id=req.user_id, room_id="xxxxx", is_win=True, rewards=999)
    return rsp
