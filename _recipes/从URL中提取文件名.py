"""
原项目 -projects/www.jmtt168.com/
功能   从URL中提取文件名
"""

from urllib.parse import urlparse, urljoin
import os

url = "https://xxx.com/images/001.jpg?token=abc123"

result = urlparse(url)
print(result)

path = result.path
print(path)

title = os.path.basename(path) # 获取路径最后一级名字
print(title)

# title = os.path.basename(urlparse(url).path)

print(urljoin(url, "/"))