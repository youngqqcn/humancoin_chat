import json
import random
import time
import pymysql

from utils.utils import create_redis_client
from datetime import datetime


def task():

    while True:
        try:
            with pymysql.connect(
                host="localhost",
                port=3306,
                user="root",
                password="ae633jmFLiAGqigSO41",
                db="humancoin",
            ) as cnx:
                rdc = create_redis_client()
                raw_msg = rdc.lpop("chatpointqueue")
                if raw_msg is None:
                    print("暂无消息处理")
                    time.sleep(1)
                    continue

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
        except Exception as e:
            print("error: {}".format(e))

    pass


def main():
    task()

if __name__ == "__main__":
    main()
