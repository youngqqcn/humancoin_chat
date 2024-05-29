import json
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.models import ResponseModel
from utils.utils import create_redis_client, create_response, logger


router = APIRouter()

class Req(BaseModel):
    user_id: str


class Resp(BaseModel):
    user_id: str
    total_chats: int
    win_chats: int
    win_rate: str


@router.post("", response_model=ResponseModel)
async def handler(req: Req):
    logger.info("请求参数: %s", req.json())
    rdc = create_redis_client()
    # 检查房间是否存在

    total = rdc.hget("chattotals", req.user_id)
    total = 0 if total is None else int(total)

    wins = rdc.hget("chatwins", req.user_id)
    wins = 0 if wins is None else int(wins)

    # 防止除0
    win_rate = '0%' if total == 0 else ( format( wins/total * 100, '.0f' )+'%' )

    rsp = Resp(user_id=req.user_id, total_chats=total, win_chats=wins, win_rate=win_rate)
    logger.info("响应内容:{}".format(rsp))
    return create_response(data=rsp)
