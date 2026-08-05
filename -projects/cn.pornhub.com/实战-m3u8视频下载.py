"""
Date: 2026-08-05
Author: zigyr
"""

from DrissionPage import ChromiumPage, ChromiumOptions
import shutil
import requests
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import os
import re
import time
from tqdm import tqdm
from lxml import etree

def downloader(title, url, session):

    headers = {
        'referer': 'https://cn.pornhub.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    }

    worker = os.path.dirname(os.path.abspath(__file__))
    out_ = os.path.join(worker, "out")
    tmp_ = os.path.join(worker, "tmp")
    if os.path.exists(tmp_):
        shutil.rmtree(tmp_)
    os.makedirs(out_, exist_ok=True)
    os.makedirs(tmp_, exist_ok=True)

    url = "https://cn.pornhub.com/view_video.php?viewkey=68ffdfaf77936"

    co = ChromiumOptions()
    # co.set_argument("--start-minimized")
    co.set_browser_path(
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    )
    co.set_user_data_path(
        r"E:\EdgeProfile"
    )
    tab = ChromiumPage(co)
    tab.listen.start("index-v1-a1.m3u8")
    tab.get(url)
    packet = tab.listen.wait(timeout=10) 
    url = packet.url


    ts_list = []
    r = session.get(
        url,
        headers=headers,
    )
    for line in r.text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            ts_list.append(urljoin(url, line))

    def download(ts):
        title = os.path.basename(urlparse(ts).path)
        content = session.get(ts, headers=headers).content
        with open(os.path.join(tmp_, title), "wb") as f:
            f.write(content)
    with ThreadPoolExecutor(5) as pool:
        for _ in tqdm(
            pool.map(download, ts_list),
            total=len(ts_list),
            desc="下载进度"
        ):
            pass


    files = os.listdir(tmp_)
    files.sort(
        key=lambda x: int(
            re.search(r"seg-(\d+)", x).group(1)
        )
    )
    with open(os.path.join(out_, title + ".ts"), "wb") as f:
        for file in files:
            with open(os.path.join(tmp_, file), "rb") as ts:
                f.write(ts.read())

    shutil.rmtree(tmp_)
    print("下载完成", title)

def main():
    import pyperclip
    text = pyperclip.paste()
    tasks = []
    for line in text.splitlines():
        line = line.strip()
        if line and line.startswith("http"):
            tasks.append(line)

    print("共解析", len(tasks), "组数据：")
    print(tasks)

    for task in tasks:
        session = requests.session()
        r = session.get(task, headers={"Accept-Encoding":"gzip, deflate"})
        tree = etree.HTML(r.text)
        title = tree.xpath("//title/text()")[0].split(" ")[0]
        print("开始下载", title)
        downloader(title, task, session)


main()