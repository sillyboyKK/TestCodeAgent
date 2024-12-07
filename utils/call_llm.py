# date:2024-12-6
# author: JKai_Huang
# introduction: LLM请求

import openai
import random

API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
BASE_URLS = ["https://api.deepseek.com"]
MODEL_NAME = ["deepseek-chat"]


# API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
# BASE_URLS = [ "https://dashscope.aliyuncs.com/compatible-mode/v1", "https://dashscope.aliyuncs.com/compatible-mode/v1"]
# MODEL_NAME = ["qwen", "qwen-max", "qwen1.5-110b-chat"]
# MODEL_NAME = ["qwen-long", "qwen-max", "qwen1.5-110b-chat"]

#使用了两个端口轮流请求
urls = BASE_URLS
url_len = len(urls)

clients = []
for base_url in urls:
    clients.append(openai.OpenAI(api_key=API_KEY, base_url=base_url))

def __select_base():
    global idx
    idx = getattr(__select_base, "idx", 0)
    print("use",urls[idx])
    i = idx
    idx = (idx + 1) % url_len
    setattr(__select_base, "index", idx)  # 保存索引
    return i


def query_llm_general(user_input):
    i = __select_base()
    try:
        completion = clients[i].chat.completions.create(
                model=MODEL_NAME[i],
                messages=user_input,
                temperature=0.7,
                # timeout=50,
                # seed=random.randint(1, 10000)
        )
        content = completion.choices[0].message.content
        return content
    except Exception as e:
        if isinstance(e, openai.APITimeoutError) and e.status == 408:
            print("-"*10 ,"请求超时", "-"*10)
            return ""  # 请求超时，重新发起请求
        else:
            raise e
