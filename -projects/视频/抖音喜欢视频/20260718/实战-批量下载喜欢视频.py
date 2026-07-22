"""
Date: 2026-07-18
Author: zigyr
"""

import requests
import json
import os


root_dir = os.path.dirname(os.path.abspath(__file__))
outp_dir = os.path.join(root_dir, "out")
os.makedirs(outp_dir, exist_ok=True)


def get_data():
    with open("3.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def parse(data):
    url_lists = []
    for aweme in data["aweme_list"]:
        # 避免图文数据的干扰
        if "video" in aweme:
            url = aweme["video"]["play_addr"]["url_list"][0] # 这里是0
            url_lists.append(url)
    return url_lists

def download(url_lists):
    for idx, url in enumerate(url_lists):
        r = requests.get(url)
        with open(os.path.join(outp_dir, f"{idx}.mp4"), "wb") as f:
            print("写入成功", idx, url)
            f.write(r.content)


def main():
    download(parse(get_data()))

if __name__ == "__main__":
    main()