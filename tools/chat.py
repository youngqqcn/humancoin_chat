import time
import requests
import jwt
import sys

import sys
sys.path.append('.')
from utils.jwt import create_jwt

host = "http://127.0.0.1:4033"


def finish_chat(user_id: str, room_id: str):
    judge = input("聊天结束,对方是人类吗? 请输入  yes 或者 no: ")
    assert judge.strip() in ["yes", "no"]
    finish_rsp = requests.post(
        f"{host}/finishChat",
        json={
            "user_id": user_id,
            "room_id": room_id,
            "human": True if judge.strip() == "yes" else False,
        },
        headers={"Content-Type": "application/json", "Human-Token": create_jwt(user_id=user_id)},
    )

    if finish_rsp is not None:
        if finish_rsp.json()["data"]["is_win"]:
            print("恭喜!你赢了!")
        else:
            print("很遗憾!你输了!")
    return


def query_chat(user_id: str, room_id: str):
    rsp = requests.post(
        f"{host}/queryChat",
        json={
            "user_id": user_id,
            "room_id": room_id,
        },
        headers={"Content-Type": "application/json", "Human-Token": create_jwt(user_id=user_id)},
    )
    if not rsp.ok:
        print("error: {}".format(rsp.text))
        exit(0)
    return rsp.json()


def send_chat(user_id: str, room_id: str, user_input: str):
    rsp = requests.post(
        f"{host}/sendChatMsg",
        json={
            "user_id": user_id,
            "msg": user_input.strip(),
            "room_id": room_id,
        },
        headers={"Content-Type": "application/json", "Human-Token": create_jwt(user_id=user_id)},
    )
    if rsp is None or rsp.status_code != 200:
        print("error: {}".format(rsp.text))
        exit(0)
    pass


def start_chat(user_id: str):
    # 开始匹配
    rsp = requests.post(
        f"{host}/startChat",
        json={"user_id": user_id},
        timeout=30,
        headers={"Content-Type": "application/json", "Human-Token": create_jwt(user_id=user_id)},
    )
    if rsp is None or rsp.status_code != 200:
        print("匹配失败:{}".format(rsp.text))
        exit(0)

    room_id = rsp.json()["data"]["room_id"]
    print("房间号: {}".format(room_id))
    return room_id


def main():

    # 输入user_id
    user_id = input("请输入用户id:")

    # 开始匹配
    room_id = start_chat(user_id=user_id)

    while True:
        while True:
            # 查询聊天
            rsp = query_chat(user_id=user_id, room_id=room_id)

            # 如果聊天已经结束
            if rsp["data"]["is_time_up"]:
                finish_chat(user_id=user_id, room_id=room_id)
                return

            # 是否轮到我发言
            if rsp["data"]["is_my_turn"]:
                if len(rsp["data"]["msgs"]) > 0:
                    latest_msg = rsp["data"]["msgs"][0]["content"]
                    print("\nOther: {}".format(latest_msg))
                break
            time.sleep(1)
            continue

        # 开始发言
        user_input = input("You 😊: ")
        if user_input == "exit":
            break
        elif len(user_input.strip()) == 0:
            continue

        # 发送消息
        send_chat(user_id=user_id, room_id=room_id, user_input=user_input)
        pass


if __name__ == "__main__":
    main()
