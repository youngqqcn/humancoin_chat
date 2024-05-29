from pprint import pprint
from openai import OpenAI


from prompts.prompt1 import system_prompt1
from prompts.prompt2 import system_prompt2
# from prompts.prompt3 import system_prompt3
# from prompts.prompt4 import system_prompt4
# from prompts.prompt5 import system_prompt5
# from prompts.prompt6 import system_prompt6


g_client = OpenAI(
    # api_key="sk-654b60ab100f44b885c5d3c004aec469", base_url="https://api.deepseek.com"
    api_key="sk-5f2e2a8929d7417487d63d1c956b2660", base_url="https://api.deepseek.com"
)
g_messages = [
    {"role": "system", "content": system_prompt2},
]


# read msg from console
if __name__ == "__main__":
    while True:
        try:
            user_input = input("You 😊: ")
            if user_input == "exit":
                break
            elif len(user_input.strip()) == 0:
                continue
            pass

            g_messages.append({"role": "user", "content": user_input})

            # print('============')
            # pprint(g_messages)
            # print('============')

            completion = g_client.chat.completions.create(
                model="deepseek-chat",
                messages=g_messages,
                temperature=1.1,
            )
            print("AI 🤖: " + completion.choices[0].message.content.strip(""))
            g_messages.append(
                {
                    "role": completion.choices[0].message.role,
                    "content": completion.choices[0].message.content.strip(),
                }
            )
        except Exception as e:
            print('hah, execuse me?')

    pass
