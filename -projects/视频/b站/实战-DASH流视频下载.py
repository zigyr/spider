"""
Date: 2026-07-18
Author: zigyr
"""

import hashlib
import json
import os
import re
import subprocess
import time

import requests
from urllib.parse import urlencode, urljoin

# ==================== 常量 ====================
PLAYURL_API = "https://api.bilibili.com/x/player/wbi/playurl"
BASE_URL = "https://www.bilibili.com"
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": BASE_URL
}

# ==================== HTTP请求 ====================
def get_response(url, params=None):
    """
    通用GET请求
    """
    return requests.get(url, headers=HEADERS, params=params)

# ==================== WBI签名 ====================
def generate_wbi_sign(params, img_key, sub_key):
    """
    B站WBI签名
    img_key + sub_key
            |
            v
       TAB重新排列
            |
            v
       截取32位
            |
            v
       mixin_key
    params + wts
            |
            v
       排序 + urlencode
            |
            v
       query + mixin_key
            |
            v
          MD5
            |
            v
          w_rid
    """
    MIXIN_KEY_ENC_TAB = [
        46,47,18,2,53,8,23,32,15,50,10,31,58,3,45,35,
        27,43,5,49,33,9,42,19,29,28,14,39,12,38,41,13,
        37,48,7,16,24,55,40,61,26,17,0,1,60,51,30,4,
        22,25,54,21,56,59,6,63,57,62,11,36,20,34,44,52
    ]
    mixin_key = ''.join(
        (img_key + sub_key)[index]
        for index in MIXIN_KEY_ENC_TAB
    )[:32]
    params["wts"] = int(time.time())
    query = urlencode(
        sorted(params.items())
    )
    params["w_rid"] = hashlib.md5(
        (query + mixin_key).encode()
    ).hexdigest()
    return params

# ==================== 下载 ====================
def download_file(url, filename):
    """
    下载m4s文件
    """
    response = requests.get(
        url,
        headers=HEADERS,
        stream=True
    )
    with open(filename, "wb") as file:
        for chunk in response.iter_content(
            chunk_size=1024 * 1024
        ):
            file.write(chunk)

# ==================== 音视频合并 ====================
def merge_video_audio(title):
    """
    使用ffmpeg合并音视频
    """
    output_folder = os.path.join(
        BASE_FOLDER,
        "out"
    )
    os.makedirs(
        output_folder,
        exist_ok=True
    )
    output_file = os.path.join(
        output_folder,
        f"{title}.mp4"
    )
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        "video.m4s",
        "-i",
        "audio.m4s",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        output_file
    ])
    os.remove("video.m4s")
    os.remove("audio.m4s")

# ==================== 主流程 ====================
def download_bilibili_video(bvid):
    # 获取视频页面
    html = get_response(urljoin(BASE_URL, bvid)).text
    # 提取页面初始化数据
    initial_state = re.search(r'__INITIAL_STATE__\s*=\s*(\{.*?\});', html, re.S)
    data = json.loads(initial_state.group(1))
    video_data = data["videoData"]
    title = re.sub(r'[\\/:*?"<>|]', "_", video_data["title"])
    print(f"视频标题: {title}")
    # WBI签名
    params = generate_wbi_sign(
        {
            "bvid": video_data["bvid"],
            "cid": video_data["cid"],
            "qn": 112,
            "fnval": 4048,
            "fnver": 0,
            "fourk": 1
        },
        data["defaultWbiKey"]["wbiImgKey"],
        data["defaultWbiKey"]["wbiSubKey"]
    )
    # 获取DASH信息
    dash = get_response(
        PLAYURL_API,
        params=params
    ).json()["data"]["dash"]
    # 选择最高码率视频和音频
    video = max(
        dash["video"],
        key=lambda item: item["bandwidth"]
    )
    audio = max(
        dash["audio"],
        key=lambda item: item["bandwidth"]
    )
    download_file(
        video["baseUrl"],
        "video.m4s"
    )
    download_file(
        audio["baseUrl"],
        "audio.m4s"
    )
    merge_video_audio(title)

def main():
    bvid = input(
        "请输入BV号: "
    )
    download_bilibili_video(bvid)
    
if __name__ == "__main__":
    main()