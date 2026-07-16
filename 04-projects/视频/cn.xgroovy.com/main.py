"""项目说明
项目说明

目标网站:
    https://cn.xgroovy.com/

项目功能:
    一个基于 Python 的 HTTP Range 多线程媒体下载器。

    通过解析视频页面获取真实媒体资源地址，
    利用 HTTP HEAD 获取文件大小，将媒体资源划分为多个字节区间，
    使用 ThreadPoolExecutor 并发下载各个分片，
    并通过随机文件写入（Random Access Write）完成最终文件重组

    当前版本支持:
    - 手动输入页面地址
    - 剪贴板批量导入（SessionBuddy）
    - 独立 Session 管理
    - 多 XPath 资源定位
    - HTTP HEAD 获取资源信息
    - HTTP Range 分块下载
    - 多线程并发下载
    - Random Access File 随机写入合并
    - 自动创建下载目录
    - 视频标题自动命名

技术栈:
| 技术                       | 用途                      |
| ------------------------ | ----------------------- |
| Python                   | 主开发语言                   |
| Requests                 | HTTP 请求、Session 管理      |
| lxml                     | HTML 文档解析               |
| XPath                    | 页面资源定位                  |
| HTTP HEAD                | 获取文件大小（Content-Length）  |
| HTTP Range               | 文件分片传输                  |
| ThreadPoolExecutor       | 多线程下载                   |
| concurrent.futures       | Future 管理、任务调度          |
| Random Access File（seek） | 随机位置写入文件                |
| os.path                  | 文件路径管理                  |
| pyperclip                | 剪贴板读取 SessionBuddy 导出内容 |
| re                       | URL 正则提取                |


"""
import requests
from lxml import etree
from concurrent.futures import as_completed, ThreadPoolExecutor
import os
import time
import pyperclip
import re

# ======================
# 1. 全局配置
# ======================
BASE_URL = "https://cn.xgroovy.com/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "out", "video")
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "referer": "https://cn.xgroovy.com/"
}

# ======================
# 2. 工具函数
# ======================
def create_filename_video(title):
    os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, f"{title}.mp4")

def create_session():
    session = requests.session()
    session.headers.update(headers)
    return session

# ======================
# 3. 页面请求
# ======================
def fetch_page(page_url, session):
    r = session.get(page_url)
    r.raise_for_status()
    return r.text

# ======================
# 4. 页面解析
# ======================
def parse_page(page_text):
    """
    获取视频所在页面的url
    通过xpath解析视频本体video_url
    """
    tree = etree.HTML(page_text)
    return tree.xpath('//*[@id="video_source_4"]/@src | //*[@id="video_source_3"]/@src')[0], tree.xpath('//title/text()')[0].split(" ")[0]

# ======================
# 5. 数据处理
# ======================
def process(data):
    """
    对数据进行加工

    比如:
    - 拼接url
    - 清洗文本
    - 生成任务
    """
    pass

# ======================
# 6. 下载/保存
# ======================
def download_range(video_url, filename, session):
    """
    针对具体的MP4_url
    进行HTTP Range 多线程下载
    """
    workers = 8

    def parse_tasks():
        """
        根据视频总大小进行解析
        返回(tasks[start, end])的信息
        方面创建线程

        args:
        workers: 线程数, 由main函数集中调度控制
        """
        r = session.head(
            video_url,
            allow_redirects=True
        )
        totals = int(r.headers.get("Content-Length"))
        block = totals // workers

        tasks = []
        for i in range(workers):
            start = i * block
            if i == workers - 1:
                end = totals - 1
            else:
                end = start + block - 1
            tasks.append((i, start, end))
        return tasks, totals

    tasks, totals = parse_tasks()

    with open(filename, "wb") as f:
        f.truncate(totals)

    def worker(index, start, end):
        range_headers  = {
            "Range": f"bytes={start}-{end}"
        }
        r = session.get(
            video_url,
            headers = range_headers ,
            stream = True
        )

        current = start

        with open(filename, "rb+") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.seek(current)
                    f.write(chunk)
                    current += len(chunk)

        return index

    
    with ThreadPoolExecutor (max_workers=workers) as executor:
        futures = [
            executor.submit(
                worker,
                index,
                start,
                end
            )
            for index, start, end in tasks
        ]

        for future in as_completed(futures):
            print(f"线程 {future.result()} 下载完成")


def batch_download(page_urls):
    for page_url in page_urls:
        start = time.time()
        session = create_session()
        page_text = fetch_page(page_url, session)
        video_url, title = parse_page(page_text)
        file_path = create_filename_video(title)
        print(f"开始下载: {file_path}")
        download_range(video_url, file_path, session)
        print(f"耗时: {time.time() - start}")
        print(f"位置: {file_path}\n")

# ======================
# 7. 主流程
# ======================
def main():
    start = time.time()

    modle = int(input("请选择网页输入方式(1.手动, 2或其他.正则匹配):"))

    if modle == 1:
        page_urls = [
            "https://cn.xgroovy.com/videos/410735/18-yo-busty-schoolgirl-takes-cumshots-on-big-ass-from-her-stepbrother/",
            "https://cn.xgroovy.com/videos/474082/chinese-babe-has-only-came-from-school-and-already-fucked-badly/",
            "https://cn.xgroovy.com/videos/380682/skinny-russian-girl-is-humping-table-and-fingerfucking-juicy-pussy/",
            "https://cn.xgroovy.com/videos/745040/pale-chick-poses-for-a-camera-with-her-round-ass-and-a-cameltoe-pussy/",
            "https://cn.xgroovy.com/videos/732142/slim-petite-teen-fingers-her-tiny-bald-pussy-gets-creamy-orgasm-in-hot-female-pov/",
            "https://cn.xgroovy.com/videos/731745/hot-close-up-panties-through-fuck-compilation-with-18yo-petite-girl/"
        ]
    else:
        """
        复制sessionbuddy的copyas`title&url`
        然后运行程序, 通过pyperclip进行读取, 避免powershell的终端输入问题
        """
        text = pyperclip.paste()
        page_urls = re.findall(r'https?://\S+', text)

    batch_download(page_urls)
    print(f"共耗时: {time.time()-start}")


if __name__ == "__main__":
    main()

"""
main()

    │

    ├──────────────┐
    │              │

手动输入URL      剪贴板读取(SessionBuddy)

    │              │

    └───────提取所有页面URL──────────┘

                    │

                    ▼

            batch_download()

                    │

        为每个页面创建独立 Session

                    │

                    ▼

              fetch_page()

                    │

             GET 获取 HTML

                    │

                    ▼

              parse_page()

                    │

         XPath 提取：

            • video_url
            • title

                    │

                    ▼

      create_filename_video()

                    │

         创建目录、生成文件名

                    │

                    ▼

           download_range()

                    │

              HEAD 请求

                    │

      获取 Content-Length

                    │

                    ▼

             计算 Range 切片

                    │

                    ▼

      ThreadPoolExecutor

        │       │       │

        ▼       ▼       ▼

     worker0 worker1 worker2 ...

        │       │       │

 GET Range0 Range1 Range2 ...

        │       │       │

        └───────┬────────┘
                │

                ▼

      Random Access Write

     seek(offset)+write()

                │

                ▼

          完整 MP4 文件
"""