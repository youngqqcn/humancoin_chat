from pprint import pprint
from typing import List
from openai import OpenAI
import asyncio

# from prompts.prompt1 import system_prompt
from .prompts.prompt2 import system_prompt


async def ai_chat(messages: List[dict]) -> str:
    g_client = OpenAI(
        api_key="sk-654b60ab100f44b885c5d3c004aec469",
        base_url="https://api.deepseek.com",  # yqq
        # api_key="sk-5f2e2a8929d7417487d63d1c956b2660", base_url="https://api.deepseek.com" # 李咏
    )
    g_messages = [
        {"role": "system", "content": system_prompt},
    ]

    g_messages.extend(messages)

    try:
        completion = g_client.chat.completions.create(
            model="deepseek-chat",
            messages=g_messages,
            temperature=1.1,
        )
        rsp_msg = completion.choices[0].message.content.strip("")
        print("AI 🤖: " + completion.choices[0].message.content.strip(""))
        return rsp_msg
    except Exception as e:
        print('error: {}'.format(e))
        return 'are you bot?'

    pass
