# date:2024-12-7
# author: JKai_Huang
# introduction: agent选择下一步执行的action

import os

from .code_agent import CodeAgent
from .static_prompt import RWRITE_CODE_GENERATOR_PROMPT, CREATE_CODE_GENERATOR_PROMPT
from utils.code_extractor import extract_markdown_code_blocks
from .sandbox import execute_file


# 分析项目结构
def analyze_project():
    pass


# 创建文件
def create_file(proj_tree:str, input_file:str=None, output_file:str=None, content:str=None):
    
    if not (output_file and content):
        return "缺乏输入，执行失败"
    
    codeGenerator = CodeAgent()
    codeGenerator_input = CREATE_CODE_GENERATOR_PROMPT.format(content, proj_tree)

    res =codeGenerator.generate_code(codeGenerator_input)
    res_code = extract_markdown_code_blocks(res)

    output_file = "./"+output_file
    if not os.path.exists(os.path.dirname(output_file)):
        print(f"不存在{output_file}，已创建")
        os.mkdir(output_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(res_code) 
    
    return "完成改写"


# 改写文件
def rewrite_file(proj_tree:str, input_file:str=None, output_file:str=None, content:str=None):
    if not (input_file and output_file and content):
        return "缺乏输入，执行失败"

    with open("./"+input_file, 'r', encoding='utf-8') as f:
        old_text = f.read()
    
    codeGenerator = CodeAgent()
    codeGenerator_input = RWRITE_CODE_GENERATOR_PROMPT.format(content, proj_tree, input_file, old_text)

    res =codeGenerator.generate_code(codeGenerator_input)
    res_code = extract_markdown_code_blocks(res)

    output_file = "./"+output_file
    if not os.path.exists(os.path.dirname(output_file)):
        print(f"不存在{output_file}，已创建")
        os.mkdir(output_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(res_code) 
    
    return "完成改写"


# 读取文件
def read_file():
    pass


# 执行debug项目
def debug_project(proj_tree:str, file:str=None):
    print("已执行")
    """
    执行的内容
    """
    res = execute_file(file)
    return res, "已执行"


functions_dict = {
    "改写文件": rewrite_file, 
    "创建文件": create_file,
    "运行项目主文件": debug_project
}



# 选择合适action执行的地方
def execute_action(proj_tree, action, functions=functions_dict):
    action_name = action.get("actionName")
    params = action.get("parm", {})
    
    # 查找与actionName匹配的函数
    func = functions.get(action_name)
    if func:
        # 如果找到了函数，则调用它并传递参数
        return func(proj_tree=proj_tree, **params)
    else:
        print(f"没有找到与动作 {action_name} 匹配的函数。")
        return None
