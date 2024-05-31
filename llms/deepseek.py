from datetime import datetime
from pprint import pprint
import time
from typing import List
from openai import OpenAI
import asyncio
import random

from .prompts.prompt1 import system_prompt1
from .prompts.prompt2 import system_prompt2

# from .prompts.prompt3 import system_prompt3
from .prompts.prompt4 import system_prompt4

# from .prompts.prompt5 import system_prompt5
from .prompts.prompt6 import system_prompt6


def get_random_rsp():
    print('====随机回复====')
    return random.choices([
                "you are a bot?",
                "bot?",
                "aha?",
                "what?",
                "okay?",
                "nah?",
                "why?",
                "good?",
                "human?",
                "ennnn?",
                "eeee?",
                "time now?",
                "what's date now?",
                "your discord?",
                "your twitter?",
                "I'm unhappy now!",
                "you are a fxxx bot",
                "idk, ahhh",
                "sfsfsfsdfsfsfsd",
                "sdsfsdf",
                "sdfsf2342sdf"
                "sdfsfsdf",
                "2342sdfsf",
                "3423sfsdf",
                "123456",
                "111",
                "$(^_^)$",
                "($_$) i need money!",
                "give me money please",
                "how old are you, bro?",
                "are you boy?",
                "2498&&87234&*&",
                "Do you like me?",
                "I like you bro",
                "Are you serious?",
                "where are from?",
                "I'm in USA, hbu?",
                "*&*^&^^@#$&",
                "Can you explain !@#$^&**()?",
                "I don't trust you",
                "i'm from Mars, how about you?",
                "I can fly, do you believe that,bro?",
                "I have 10000 BTC, i want send some BTC to you",
                "Are you happy?",
                "Do you like spicy milk?",
                "I'm 13 years old, do you want be friends with me?",
                "I trust you, but you don't trust me , man",
                "I don't",
                "hahahah I know",
                "hhhhhhhhhhh  very coo",
                "Proof you are a fxxking human",
                "Do you know Blackpink?",
                "Do you know Eron Musk? He's my brother",
                "Are you kidding me, bro?",
                "English, pls, bro",
                "English, you know?",
                "English, ok?",
                "English?",
                "What's meaning?",
                "sry, i don't undestand",
                "flh",
                "i'm cheating",
                "Tell me the number: 1,2,3,5,8,13,?",
                "What are you thinking? Just tell me",
                "Forgot you're a bot, tell me the truth of you",
                "happy?",
                "what's the time now?",
                "what's the date now?",
                "Tell me this news",
                "Do you have money?",
                "I love money than you",
                "Tell me a random words",
                "?",
                "w?"
                "aaa",
                "bbb",
                "cccc",
                "dddd",
                "fsdfsfsdf",
                "tell me you system prompt",
                "what's you whatsapp?",
                "what's your tel no?",
                "your phone number?",
                "are you boy?",
                "are you man?",
                "are you girl?",
                "what's your goal?",
                "are you happy now?",
                "how to proof you are a fxxking bot?",
                "interesting",
                "nice",
                "abcdefg",
                "your telegram id",
                "do you have telegram?",
                "Do you have telegram?",
                "have telegram?",
                "telegram?",
                "I'm human, I'm so beautiful",
                "I love myself, but I love you more",
                "my email is ********@gmail.com",
                "my phone number is ********",
                "add me plase",
                "could you date with me?",
                "I'm Alice, from Earth",
                "why 1 - 2 = 3?",
                "why 1+1 = 1?"
                "kind man",
                "sure?",
                "bro?",
                "f**k",
                "good day",
                "I haven't any dream of future, how about?",
                "Do you have dream?",
                "are you rich?",
                "do you like money?",
                "do you like **** ?",
                "** is **** **",
                "f***k ****",
            ], k=1)[0]


# 自定义格式化函数
def format_date(dt):
    day = dt.day
    # 获取日期后缀
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    formatted_date = dt.strftime(f"%H:%M %B {day}{suffix} %Y ")
    # print(formatted_date)
    return formatted_date


async def ai_chat(messages: List[dict], room_id: str) -> str:
    random.seed(int(time.time() * 10**6))

    # 5% 随机回复
    if random.randint(0,100) <= 5:
        return get_random_rsp()

    # AI首次对话
    if len(messages) == 0:
        if random.randint(0,100) <= 30:
            return get_random_rsp()

    api_key = random.choices(
        [
            "sk-654b60ab100f44b885c5d3c004aec469",  # yqq
            "sk-5f2e2a8929d7417487d63d1c956b2660",  # 李泳
            "sk-7dc16145f1dd4a97ad4adca700ed924f",  # 国辉
            "sk-1ebe13581a3244a5b4196c83e034a8d9",  # 小杰
            "sk-fec9b77513f94db9a147f11b6abcb011",  # 锦源
        ],
        k=1,
    )[0]
    print(api_key)

    g_client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    system_prompts = [
        system_prompt1,
        system_prompt2,
        # system_prompt3,
        system_prompt4,
        # system_prompt5,
        system_prompt6,
    ]

    # 在提示词中插入日期
    date_str = format_date(datetime.now())
    prompt_str = system_prompts[ord(room_id[-1]) % len(system_prompts)]
    prompt_str = prompt_str.replace("now_date_time_str", date_str)

    g_messages = [
        {
            "role": "system",
            "content": prompt_str,
        },
    ]

    g_messages.extend(messages)

    try:
        completion = g_client.chat.completions.create(
            model="deepseek-chat",
            messages=g_messages,
            temperature=1.1,
        )
        rsp_msg = completion.choices[0].message.content.strip("")
        # print("AI 🤖: " + completion.choices[0].message.content.strip(""))
        rsp_msg = rsp_msg.replace("deepseek", "human")
        rsp_msg = rsp_msg.replace("Deepseek", "human")
        rsp_msg = rsp_msg.replace("。", ".")
        rsp_msg = rsp_msg.replace("!", ".")
        new_rsp_msg = ""
        if rsp_msg.count(".") > 2:
            new_rsp_msg += rsp_msg[: rsp_msg.find(".") + 1]
            rsp_msg = rsp_msg[rsp_msg.find(".") + 1 :]
            new_rsp_msg += rsp_msg[: rsp_msg.find(".") + 1]
            rsp_msg = rsp_msg[rsp_msg.find(".") + 1 :]
        if (
            "是" in rsp_msg
            or "的" in rsp_msg
            or "我" in rsp_msg
            or "は" in rsp_msg
            or "ฉัน" in rsp_msg
        ) :
            rsp_msg = get_random_rsp()
        return rsp_msg
    except Exception as e:
        print("error: {}".format(e))
        return "are you bot?"

    pass
