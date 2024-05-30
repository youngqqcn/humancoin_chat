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


async def ai_chat(messages: List[dict], room_id: str) -> str:
    random.seed(int(time.time() * 10**6))
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

    g_messages = [
        {
            "role": "system",
            "content": system_prompts[ord(room_id[-1]) % len(system_prompts)],
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
        return rsp_msg
    except Exception as e:
        print("error: {}".format(e))
        return "are you bot?"

    pass
