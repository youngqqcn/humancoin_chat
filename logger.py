import logging

# 创建日志记录器
logger = logging.getLogger("my_fastapi_app")
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建控制台处理器并设置日志级别
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建文件处理器并设置日志级别
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

# 创建格式化器并将其添加到处理器中
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到记录器中
logger.addHandler(console_handler)
logger.addHandler(file_handler)