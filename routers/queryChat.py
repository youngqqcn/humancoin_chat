from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Req(BaseModel):
    user_id: str
    room_id: str


class Msg(BaseModel):
    msg: str
    id: str
    user: str


class Resp(BaseModel):

    user_id: str
    room_id: str
    msgs: List[Msg]


@router.post("", response_model=Resp)
async def handler(req: Req):
    rsp = Resp(
        user_id=req.user_id, room_id="xxxxx", msgs=[Msg(msg="hello", id="1", user="A")]
    )
    return rsp
