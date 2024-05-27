import time
import requests

def finish_chat(user_id: str, room_id: str):
    judge = input("聊天结束,对方是人类吗? 请输入  yes 或者 no: ")
    assert judge.strip() in ["yes", "no"]
    finish_rsp = requests.post(
        "http://192.168.110.207:8000/finishChat",
        json={
            "user_id": user_id,
            "room_id": room_id,
            "human": True if judge.strip() == "yes" else False,
        },
    )

    if finish_rsp is not None:
        if finish_rsp.json()["data"]["is_win"]:
            print("恭喜!你赢了!")
        else:
            print("很遗憾!你输了!")
    return


def query_chat(user_id: str, room_id: str):
    rsp = requests.post(
        "http://192.168.110.207:8000/queryChat",
        json={
            "user_id": user_id,
            "room_id": room_id,
        },
    )
    if not rsp.ok:
        print("error: {}".format(rsp.text))
        exit(0)
    return rsp.json()


def send_chat(user_id: str, room_id: str, user_input: str):
    rsp = requests.post(
        "http://192.168.110.207:8000/sendChatMsg",
        json={
            "user_id": user_id,
            "msg": user_input.strip(),
            "room_id": room_id,
        },
    )
    if rsp is None or rsp.status_code != 200:
        print("error: {}".format(rsp.text))
        exit(0)
    pass


def main():

    # 输入user_id
    user_id = input("请输入用户id:")

    # 开始匹配
    rsp = requests.post(
        "http://192.168.110.207:8000/startChat", json={"user_id": user_id}, timeout=30
    )
    if rsp is None or rsp.status_code != 200:
        print("匹配失败:{}".format(rsp.text))
        exit(0)

    room_id = rsp.json()["data"]["room_id"]
    print("房间号: {}".format(room_id))
    while True:
        waiting_msg = False
        while True:
            rsp = query_chat(user_id=user_id, room_id=room_id)
            # 如果聊天已经结束
            if rsp["data"]["is_time_up"]:
                finish_chat(user_id=user_id, room_id=room_id)
                return

            if rsp["data"]["is_my_turn"]:
                if len(rsp["data"]["msgs"]) > 0:
                    latest_msg = rsp["data"]["msgs"][0]["content"]
                    print("\nOther: {}".format(latest_msg))
                break

            if not waiting_msg:
                print("等待对方回复." , end='')
                waiting_msg = True
            else:
                print("..", end='')
            time.sleep(1)
            continue

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
