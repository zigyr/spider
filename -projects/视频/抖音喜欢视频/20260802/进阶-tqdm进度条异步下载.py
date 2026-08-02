import json
import os

worker_folder = os.path.dirname(os.path.abspath(__file__))
out_ = os.path.join(worker_folder, "out")
os.makedirs(out_, exist_ok=True)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.douyin.com/",
}

with open(os.path.join(worker_folder, "video.json"), "r", encoding="utf-8") as f:
    video_list = json.load(f)

# for video in video_list:
#     print(video["title"], video["url"])

import aiohttp
import aiofiles
import os
import re
import asyncio

def clean_filename(title):
    name = re.sub(r'[\\/:*_?"<>|]', ' ', title) # 特殊字符
    name = re.sub(r'\s+', ' ', name) # 多余空格
    name = name.strip() # 前后空格
    return name[:100] # 长度限制


limit = asyncio.Semaphore(10) # 同时最多10个视频下载
max_retry = 3 # 最大retry次数
async def download_one(session, video):
    async with limit:
        title = clean_filename(video["title"])
        url = video["url"]
        file_path = os.path.join(out_, f"{title}_{video['id']}.mp4")

        for retry in range(max_retry):
            async with session.get(url) as r:
                if r.status == 200:
                    async with aiofiles.open(file_path, "wb") as f:
                        async for chunk in r.content.iter_chunked(1024*1024):
                            await f.write(chunk)
                    return True
                else:
                    print(f"{title} 状态码错误:{r.status}")
                    await asyncio.sleep(2**retry)
        print("放弃下载:", title, url)
        return False


from tqdm.asyncio import tqdm_asyncio
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for video in video_list:
            task =  asyncio.create_task(
                download_one(session, video)
            )
            tasks.append(task)
        results = await tqdm_asyncio.gather(*tasks, desc="下载进度")
        success = results.count(True)
        failed = results.count(False)
        print(f"下载完成 成功:{success} 失败:{failed}")

if __name__ == "__main__":
    asyncio.run(main())
        