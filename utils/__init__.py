from utils.redis import create_redis_client
from .reponse import HcError, ResponseModel, create_response
from .hcjwt import verify_jwt
from .exceptions import http_exception_handler, general_exception_handler
import logging


logger = logging.getLogger("humancoin")
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建控制台处理器并设置日志级别
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建文件处理器并设置日志级别
# file_handler = logging.FileHandler("app.log")
# file_handler.setLevel(logging.INFO)

# 创建格式化器并将其添加到处理器中
formatter = logging.Formatter(
    "%(levelname)s : %(asctime)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s"
)
console_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)

# 将处理器添加到记录器中
logger.addHandler(console_handler)
# logger.addHandler(file_handler)


__all__ = [
    http_exception_handler,
    general_exception_handler,
    verify_jwt,
    ResponseModel,
    create_redis_client,
    create_response,
    HcError,
    logger
]

