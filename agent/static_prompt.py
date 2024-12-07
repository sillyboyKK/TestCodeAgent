# date:2024-12-7
# author: JKai_Huang
# introduction: 静态prompt模板

ACTION_LIST_PROMPT = [
    {
        "actionName": "改写文件",
        "parm": {
            "input_file": "<输入文件的路径>",
            "output_file": "<输出文件的路径>",
            "content": "<需要改写文件内容的要求>"
        }
    },
    {
        "actionName": "创建文件",
        "parm": {
            "input_file": "<输入文件的路径>",
            "output_file": "<输出文件的路径>",
            "content": "<需要创建文件内容的要求>"
        }
    },
    {
        "actionName": "运行项目主文件",
        "parm": {
            "file": "<需要运行的主文件的路径>"
        }
    }
]


ROUGH_TASK_SPLIT_PROMPT = """
【要求】：{} 
以下是项目的文件结构：
{} 
【输出要求】：请输出完成要求的具体步骤。具体的步骤，一定要按照【输出格式】，以列表的形式按顺序输出
【输出格式】["步骤1", "步骤2", ...]
"""

FINE_TASK_SPLIT_PROMPT = """
【要求】：{}
以下是项目的文件结构：
{} 
【可选择的操作】:{}
【输出要求】：请按照要求，从【可选择的操作】中选择几个具体操作来完成要求。具体的操作，一定要按照【输出格式】，以列表的形式按顺序输出。
【输出格式】：
[{{
    "actionName": "<操作的名字>",
    "parm": {{
        <对应操作的参数>
    }}
}}, 
...]
"""

RWRITE_CODE_GENERATOR_PROMPT = """
【要求】：{} 
以下是项目的文件结构：
{} 
打开文件'{}'的内容如下：
{}
【输出要求】：输出代码
"""

CREATE_CODE_GENERATOR_PROMPT = """
【要求】：{} 
以下是项目的文件结构：
{}
【输出要求】：输出代码
"""