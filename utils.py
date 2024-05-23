from redis import Redis
from models import ResponseModel

def create_response(data: any = None, msg: str = "ok", code: int = 0):
    return ResponseModel(code=code, msg=msg, data=data)



def create_redis_client() -> Redis:
    return Redis(
        host="localhost",
        port=6379,
        password="gooDluck4u",
        db=0,
        decode_responses=True,  # 自动解码响应
    )