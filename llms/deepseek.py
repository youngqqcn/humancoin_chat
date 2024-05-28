from pprint import pprint
import time
from typing import List
from openai import OpenAI
import asyncio
import random

from .prompts.prompt1 import system_prompt1
from .prompts.prompt2 import system_prompt2
from .prompts.prompt3 import system_prompt3


async def ai_chat(messages: List[dict], room_id: str) -> str:
    random.seed(int(time.time() * 10**6))
    g_client = OpenAI(
        api_key=random.choices(
            [
                "sk-654b60ab100f44b885c5d3c004aec469",  # yqq
                "sk-5f2e2a8929d7417487d63d1c956b2660",  # 李泳
            ],
            k=1,
        )[0],
        base_url="https://api.deepseek.com",
    )

    system_prompts = [system_prompt1, system_prompt2, system_prompt3]

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
