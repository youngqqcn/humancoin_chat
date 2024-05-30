

import logging


# def get_logger(logger_name = 'hc'):
#     logger = logging.getLogger("humancoin")
#     logger.setLevel(logging.DEBUG)  # 设置日志级别

#     # 创建控制台处理器并设置日志级别
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.DEBUG)

#     # 创建文件处理器并设置日志级别
#     # file_handler = logging.FileHandler("app.log")
#     # file_handler.setLevel(logging.INFO)

#     # 创建格式化器并将其添加到处理器中
#     formatter = logging.Formatter(
#         "%(levelname)s : %(asctime)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s"
#     )
#     console_handler.setFormatter(formatter)
#     # file_handler.setFormatter(formatter)

#     # 将处理器添加到记录器中
#     logger.addHandler(console_handler)
#     # logger.addHandler(file_handler)

import logging
# 既把日志输出到控制台， 还要写入日志文件
class HcLogger():
    def __init__(self, logname="hcloger", loglevel=logging.INFO, loggername="hcloger"):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(loglevel)
        # 创建一个handler，用于写入日志文件
        # fh = logging.FileHandler(logname)
        # fh.setLevel(loglevel)
        if not self.logger.handlers:
            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            # 定义handler的输出格式
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            formatter = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)s:%(lineno)d: %(message)s')
            # fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # 给logger添加handler
            # self.logger.addHandler(fh)
            self.logger.addHandler(ch)
    def getlog(self):
        return self.logger