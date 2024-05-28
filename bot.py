import asyncio
import json
import time
import uuid


from llms.deepseek import ai_chat
from utils.utils import create_redis_client


#
async def chat_handler(tid: int, room_id: str):
    try:
        rdc = create_redis_client()

        # 查询消息记录
        msgs = rdc.zrange("chatchannel:" + room_id, 0, -1, desc=False)
        history_msgs = []
        if msgs is None or len(msgs) == 0:
            #  AI说第一句话, 让AI先问一个问题
            history_msgs.append(
                {
                    "role": "user",
                    "content": "ask me a good question which can proof you are a human is instead of a bot",
                }
            )
            pass
        else:
            for item in msgs:
                msg = json.loads(item)
                role = "assistant" if str(msg["user_id"]).startswith("bot") else "user"
                history_msgs.append({"role": role, "content": msg["content"]})

        rsp_text = await ai_chat(messages=history_msgs, room_id=room_id)
        print("AI: {}".format(rsp_text))

        # 将AI回复的消息插入队列
        bot_user_id = rdc.hget("chatturnmutex", room_id)

        # 将消息插入
        ts = int(time.time())
        msg_id = str(uuid.uuid4())
        msg = {
            "user_id": bot_user_id,
            "content": rsp_text,
            "timestamp": ts,
            "msg_id": msg_id,
        }
        rdc.zadd("chatchannel:" + room_id, {json.dumps(msg): ts})

        # 获取该用户的对手
        room_members = rdc.lrange("chatroommembers:" + room_id, 0, -1)
        opponent_user_id = (
            room_members[0] if room_members[0] != bot_user_id else room_members[1]
        )
        # 切换当前发言人
        rdc.hset("chatturnmutex", room_id, opponent_user_id)
    except Exception as e:
        print("========= error: {}".format(e))
    pass


async def main():

    rdc = create_redis_client()
    count = 0
    while True:
        await asyncio.sleep(0.1)

        room_id = rdc.lpop("chataimsgqueue")
        if room_id is None:
            continue

        try:
            task = asyncio.create_task(chat_handler(tid=count, room_id=room_id))
        except Exception as e:
            print("error: {}".format(e))
            pass
        count += 1


asyncio.run(main())
