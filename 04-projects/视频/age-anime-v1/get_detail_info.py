import requests
import re

def get_detail_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    html = response.text

    # 1. 提取 视频名
    title_pattern = re.search(r'<title>(.*?)</title>', html, re.DOTALL)

    full_title = title_pattern.group(1).strip()
    
    anime_title = re.split(r'第|集|-|在线播放|AGE动漫', full_title)[0].strip()

    # 2. 提取 集数
    episode = url.strip("/").split("/")[-1]

    # 3. 拼接最终文件名
    filename = f"{anime_title}_第{episode}集.mp4"

    return anime_title, episode, filename