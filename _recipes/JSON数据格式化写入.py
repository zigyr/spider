"""
原项目 -projects/视频/b站视频/
功能   JSON数据以可读格式写入文件（ensure_ascii=False + indent=4）
"""

import requests
import re
import json
import time
import hashlib
import subprocess
import os
from urllib.parse import urlencode, urljoin

BASE_URL = "https://www.bilibili.com"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": BASE_URL
}

html = requests.get(urljoin(BASE_URL, "BV14iKU6eEBC"), headers=headers).text

data = json.loads(re.search(
    r'__INITIAL_STATE__\s*=\s*(\{.*?\});',
    html,
    re.S
).group(1))


with open("1.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)