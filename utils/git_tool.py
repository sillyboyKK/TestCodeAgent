# -*- coding: utf-8 -*-
# date:2024-12-6
# author: JKai_Huang
# introduction: 用于clone 给出的github项目文件的工具

# import git

# # clone代码工具
# def clone_repo(repo_url:str, local_dir:str)->bool:
#     """
#     repo_url: github project url
#     local_dir: clone to local dir
#     """
#     try:
#         git.Repo.clone_from(repo_url, local_dir)
#         print(f"Repository cloned to {local_dir}")
#         return True
#     except git.exc.GitError as e:
#         print(f"Failed to clone repository: {e}")
#         return False
    
import subprocess

def clone_repo(repo_url:str, dest_path:str)->bool:
    try:
        # 执行git clone命令
        result = subprocess.run(['git', 'clone', repo_url, dest_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Clone {repo_url} successful!")
            return True
        else:
            print(f"Clone {repo_url} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Clone {repo_url} failed: {e}")
        return False