from utils.call_llm import query_llm_general
from utils.code_extractor import extract_markdown_code_blocks


class CodeAgent:
    def __init__(self):
        self.input = [{"role": "system", "content": "你是一个python游戏工程师"}]
        self.query = {"role": "user", "content": ""}
        self.answer = {"role": "assistant", "content": ""}
        self.konwledge = ""

    def generate_code(self, user_input):
        # 添加对话历史
        self.query['content'] = user_input
        self.input.append(self.query)

        res = query_llm_general(self.input)
        self.answer['content'] = res
        self.input.append(self.answer)

        # return extract_markdown_code_blocks(res)
        return res
    


    
