from typing import Union
from redis import Redis


from utils.reponse import ResponseModel
import logging




def create_redis_client(db=1) -> Redis:
    return Redis(
        host="localhost",
        port=6379,
        password="gooDluck4u",
        db=db,
        decode_responses=True,  # 自动解码响应
    )




