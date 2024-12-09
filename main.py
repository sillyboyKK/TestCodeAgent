# date:2024-12-6
# author: JKai_Huang
# introduction: 主程序， 游戏自动化生成pipeline

from agent.code_agent import CodeAgent
from agent.sandbox import Sandbox, LocalSandbox, execute_file
from agent.static_prompt import *
from agent.action import *
from utils.content_tool import sanitize_input, get_directory_tree, get_json_from_text
from utils.git_tool import clone_repo
import os

def main():
    print("Welcome to the Code Agent!")
    # git_url = input("Please give the URL of the github project: ")
    # clone_dir = input("Please give the path to clone to the local: ")
    
    git_url = "https://github.com/mumuy/pacman.git"
    clone_dir = "F:/Project/AgentProject/MyCodeAgent/tmp_project/"

    if not os.path.exists(clone_dir):
        res = clone_repo(git_url, clone_dir)
        if not res:
            print("git clone失败")
            return
    
    
    res_tree = get_directory_tree(clone_dir)

    user_input = "将这个项目迁移到python语言运行，并将index.js中map的地图数据改为sqlite存取，根据游戏代码，给这个游戏编写一份详细的游戏玩法说明书。"

    # user_input = input("Please describe what you want the code to do: ")
    sanitized_input =  ROUGH_TASK_SPLIT_PROMPT.format(sanitize_input(user_input), res_tree)

    generator = CodeAgent()
    roughTask_list = generator.generate_code(sanitized_input)
    print("\nGenerated Code:\n")
    print(roughTask_list)
    print(type(roughTask_list))

    roughTask_list = get_json_from_text(roughTask_list)

    generator_fine = CodeAgent()

    for roughTask  in roughTask_list[0:1]:
        print("【任务】：" + roughTask)
        fineTask_input = FINE_TASK_SPLIT_PROMPT.format(roughTask, res_tree, ACTION_LIST_PROMPT)
        res_fineTask = generator_fine.generate_code(fineTask_input)
        print("【输出】：" + res_fineTask)
        fineTask_list =  get_json_from_text(res_fineTask)

        fb = ""
        fw = ""

        for fineTask in fineTask_list:
            flag, res = execute_action(res_tree, fineTask, forward=fw)
            print(res)
            while not flag:
                usr_i = input("是否继续重新执行该操作[Y/N]：")
                if usr_i.lower() == "y":
                    fb = res
                    flag, res = execute_action(res_tree, fineTask, feedback=fb, forward=fw)
                    print(res)
                elif usr_i.lower() == "n":
                    break
                else:
                    usr_i = input("输入有误，请重新选择[Y/N]：")
            fw = res






    # sandbox = LocalSandbox()
    # execution_result = sandbox.execute_code(generated_code)
    # print("\nExecution Result:\n")
    # print(execution_result)

if __name__ == "__main__":
    main()
    # print(execute_file("tmp_project/static/script/index.py"))

