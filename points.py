import json
import random
import time
import pymysql

from utils.utils import create_redis_client
from datetime import datetime
import argparse


class MySqlConfig:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db


def task(config: MySqlConfig):

    while True:
        try:
            rdc = create_redis_client()
            raw_msg = rdc.lpop("chatpointqueue")
            if raw_msg is None:
                # print("暂无消息处理")
                time.sleep(1)
                continue
            print('消息:{}'.format(raw_msg))

            with pymysql.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                db=config.db,
            ) as cnx:
                with cnx.cursor() as cursor:
                    msg = json.loads(raw_msg)
                    print("消息: {}".format(msg))

                    points = msg["points"]
                    user_id = msg["user_id"]
                    time_str = datetime.fromtimestamp(msg["timestamp"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if points == 0:
                        print("忽略积分为0")
                        continue

                    # 更新用户积分余额
                    operator = "+" if points > 0 else "-"
                    sql_str = f"""
                        UPDATE user_integral_wallet
                        SET balance = IF(balance {operator} {points} >= 0, balance {operator} {points}, 0)
                        WHERE user_id='{user_id}';
                        """
                    print(sql_str)
                    ret = cursor.execute(sql_str)
                    print("ret = {}".format(ret))
                    cnx.commit()

                    # 插入积分记录
                    id = str(int(time.time() * 10**6)) + str(
                        random.randint(10000, 99999)
                    )
                    biz_id = "humancoin_chat"
                    trade_type = 3  # '交易类型 1:活动奖励, 2:游戏参与, 3:游戏奖励'
                    insert_sql_str = f"""
                    INSERT INTO user_point_record(`id`, `biz_id`, `trade_type`, `user_id`, `amount`, `create_time`)
                    VALUES('{id}', '{biz_id}', {trade_type}, '{user_id}', {points}, '{time_str}')
                    """
                    cursor.execute(insert_sql_str)
                    cnx.commit()
                    print('消息处理完成')
        except Exception as e:
            print("error: {}".format(e))

    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, help="test or pro")
    args = parser.parse_args()

    if args.env == "test":
        mysql_config = MySqlConfig(
            host="localhost",
            port=3306,
            user="root",
            password="ae633jmFLiAGqigSO41",
            db="tg_server_db",
        )
        task(mysql_config)
    elif args.env == "pro":
        mysql_config = MySqlConfig(
            host="fansland-pro-mysql.cluster-cdm88s6ekcfi.ap-southeast-1.rds.amazonaws.com",
            port=3306,
            user="admin",
            password="ae633jmFLiAGqigSO42",
            db="tg_server_db",
        )
        task(mysql_config)
    else:
        raise "invalid env"


if __name__ == "__main__":
    main()
