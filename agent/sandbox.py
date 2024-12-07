# date:2024-12-7
# author: JKai_Huang
# introduction: 用于运行程序的沙盒

import docker
import tempfile
import os
import subprocess


class Sandbox:
    def __init__(self):
        self.client = docker.from_env()
        self.image = os.getenv('DOCKER_IMAGE')

    def execute_code(self, code):
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp.write(code.encode())
            temp_path = temp.name

        try:
            container = self.client.containers.run(
                self.image,
                command=f'python {temp_path}',
                volumes={os.path.dirname(temp_path): {'bind': '/tmp', 'mode': 'ro'}},
                working_dir='/tmp',
                stderr=True,
                stdout=True,
                detach=True
            )
            output = container.wait()
            logs = container.logs().decode()
            return logs
        finally:
            os.remove(temp_path)
            if 'container' in locals():
                container.remove(force=True)


class LocalSandbox:
    def __init__(self):
        pass

    def execute_code(self, code):
        # 将Python代码写入临时文件
        with open('./tmp/temp_script.py', 'w') as file:
            file.write(code)

        try:
            # 调用CMD执行Python程序并传入临时文件路径
            result = subprocess.run(
                ['python', './tmp/temp_script.py'],  # 假设Python解释器在系统环境变量PATH中
                capture_output=True,           # 捕获标准输出和标准错误
                text=True,                     # 返回str而不是bytes
                check=True                     # 如果子进程退出时返回非零值，则抛出CalledProcessError
            )

            # 打印标准输出
            print("Standard output:", result.stdout)
            # 如果有错误信息，打印标准错误
            if result.stderr:
                print("Standard error:", result.stderr)
            
            return result

        finally:
            # 清理：删除临时文件
            import os
            if os.path.exists('./tmp/temp_script.py'):
                os.remove('./tmp/temp_script.py')


def execute_file(file):
    _, ext = os.path.splitext(file)

    if ext.lower() == '.py':
        # 调用CMD执行Python程序并传入临时文件路径
        result = subprocess.run(
            ['python', file],  # 假设Python解释器在系统环境变量PATH中
            capture_output=True,           # 捕获标准输出和标准错误
            text=True,                     # 返回str而不是bytes
            check=True                     # 如果子进程退出时返回非零值，则抛出CalledProcessError
        )

        # 打印标准输出
        print("Standard output:", result.stdout)
        # 如果有错误信息，打印标准错误
        if result.stderr:
            print("Standard error:", result.stderr)
        
        return result