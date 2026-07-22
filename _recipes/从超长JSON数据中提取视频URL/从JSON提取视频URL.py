"""
原项目 -projects/视频/抖音喜欢视频/
功能   从抖音API返回的JSON中解析提取视频URL列表
"""

import json
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(root_dir, "1.json")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# for i in range(4, 20):
#     url = data["aweme_list"][i]["video"]["play_addr"]["url_list"][1]
#     print(i, url)

url_lists = []
for aweme in data["aweme_list"]:
    # 避免图文数据的干扰
    if "video" in aweme:
        url = aweme["video"]["play_addr"]["url_list"][0]
        url_lists.append(url)
print(len(url_lists))