# -*- coding: utf-8 -*-
# date:2024-12-7
# author: JKai_Huang
# introduction: 解析输出中代码块

import mistune

# 创建一个自定义渲染器，用于收集 Python 代码块
class CodeBlockCollector(mistune.HTMLRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code_blocks = []

    def block_code(self, code, info=None):
        # 如果提供了语言信息并且是 'python'，则保存代码块
        if info and info.strip().lower() == 'python':
            self.code_blocks.append(code)
        return ''  # 不需要生成 HTML 输出

def extract_markdown_code_blocks(text):
    # 创建带有自定义渲染器的 Markdown 解析器
    renderer = CodeBlockCollector(escape=True)
    markdown_parser = mistune.create_markdown(renderer=renderer)

    # 解析 Markdown 文本
    markdown_parser(text)

    # 返回所有收集到的 Python 代码块，用换行符连接
    return '\n'.join(renderer.code_blocks)