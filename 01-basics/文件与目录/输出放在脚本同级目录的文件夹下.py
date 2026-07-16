import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "out")
os.makedirs(output_dir, exist_ok=True) # 避免文件已存时是报错

for i in range(10):
    file_path = os.path.join(output_dir, str(i)+'.txt')
    with open(file_path, "w") as f:
        f.write(str(i))