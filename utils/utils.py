from redis import Redis
from models.models import ResponseModel
import logging

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



# 创建日志记录器
logger = logging.getLogger('humancoin')
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建控制台处理器并设置日志级别
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建文件处理器并设置日志级别
# file_handler = logging.FileHandler("app.log")
# file_handler.setLevel(logging.INFO)

# 创建格式化器并将其添加到处理器中
formatter = logging.Formatter('%(levelname)s : %(asctime)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s')
console_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)

# 将处理器添加到记录器中
logger.addHandler(console_handler)
# logger.addHandler(file_handler)