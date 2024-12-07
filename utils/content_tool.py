# -*- coding: utf-8 -*-
# date:2024-12-7
# author: JKai_Huang
# introduction: 用于内容的后处理，包括输入的清洗，输出的格式化或解析

from pathlib import Path
import json
import re


def sanitize_input(user_input):
    # 实现一些基本的输入清理和验证逻辑
    return user_input.strip()


def get_directory_tree(root, prefix='', is_last=True):
    # 创建一个列表来保存每一行的字符串
    tree_lines = []

    # 如果是根目录，添加目录名到列表中
    if isinstance(root, str):
        root = Path(root)
    if root.parent != root:
        tree_lines.append(f'{prefix}{"└── " if is_last else "├── "}{root.name}/')
    else:
        tree_lines.append(f'{root.name}/')

    # 更新前缀以反映层级关系
    prefix += '    ' if is_last else '|   '

    # 获取排序后的条目（先目录后文件）
    entries = sorted(root.iterdir(), key=lambda e: (not e.is_dir(), e.name))

    # 遍历条目
    for i, entry in enumerate(entries):
        is_last_entry = i == len(entries) - 1
        new_prefix = '    ' if is_last_entry else '|   '
        if entry.is_dir():
            # 递归处理子目录
            subtree_lines = get_directory_tree(entry, prefix, is_last_entry)
            tree_lines.extend(subtree_lines)
        else:
            # 处理文件
            tree_lines.append(f'{prefix}{"└── " if is_last_entry else "├── "}{entry.name}')

    return tree_lines


# 将列表转换为单个字符串
def directory_tree_to_string(root):
    tree_lines = get_directory_tree(Path(root))
    return '\n'.join(tree_lines)


# 提取文本中的json
def get_json_from_text(text:str):

    try:
        result_list = json.loads(text)
        # print("处理方法1：", result_list)
        return result_list

    except:
        # 定义一个正则表达式模式来匹配 ```json 和 ``` 之间的所有内容
        pattern = r'```json(.*?)```'
        
        # 使用re.findall()查找所有匹配项，并设置flags=re.DOTALL以使.可以匹配换行符
        matches = re.findall(pattern, text, flags=re.DOTALL)
        match = None
        for item in matches:
            if item:
                match = item
                break

        if match:
        # 提取的内容
            try:
                result_list = json.loads(match)
                # print("处理方法2：", result_list)
                return result_list

            except:

                # 使用正则表达式查找JSON数组
                match = re.search(r'$(.*?)$', text)

                if match:
                    # 匹配到的内容已经是有效的JSON数组字符串
                    json_str = '[' + match.group(1) + ']'
                    
                    try:
                        result_list = json.loads(json_str)
                        # print("处理方法3：", result_list)
                        return result_list
                    except json.JSONDecodeError as e:
                        print("JSON解析错误:", e)
                        return None
                else:
                    print("没有找到符合的列表")
                    return None
        else:
            print("没有找到符合的列表")
            return None




# # 使用示例
# if __name__ == '__main__':
#     root_path = 'F:\\Project/AgentProject/MyCodeAgent'  # 替换为你要查看的目录路径
#     tree_str = directory_tree_to_string(root_path)
#     print(tree_str)