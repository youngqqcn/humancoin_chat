import time
import requests

# read msg from console
if __name__ == "__main__":

    # 输入user_id
    user_id = input("please input your userid:")

    # 开始匹配
    rsp = requests.post(
        "http://127.0.0.1:8000/startChat", json={"user_id": user_id}, timeout=30
    )
    if rsp is None or rsp.status_code != 200:
        print("匹配失败:{}".format(rsp.text))
        exit(0)

    room_id = rsp.json()["data"]["room_id"]
    print("房间号: {}".format(room_id))
    while True:
        while True:
            rsp = requests.post(
                "http://127.0.0.1:8000/queryChat",
                json={
                    "user_id": user_id,
                    "room_id": room_id,
                },
            )
            if not rsp.ok:
                print("error: {}".format(rsp.text))
                exit(0)

            if rsp.json()["data"]["is_my_turn"]:
                if len(rsp.json()["data"]["msgs"]) > 0:
                    latest_msg = rsp.json()["data"]["msgs"][0]['content']
                    print("Other: {}".format(latest_msg))
                break

            time.sleep(1)
            continue

        user_input = input("You 😊: ")
        if user_input == "exit":
            break
        elif len(user_input.strip()) == 0:
            continue
        # print(user_input)

        rsp = requests.post(
            "http://127.0.0.1:8000/sendChatMsg",
            json={
                "user_id": user_id,
                "msg":  user_input.strip(),
                "room_id": room_id,
            },
        )
        if rsp is None or rsp.status_code != 200:
            print("error: {}".format(rsp.text))
            exit(0)
        pass
