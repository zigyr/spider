
from queue import Queue
import threading
import requests  
from lxml import etree
import re
import os
from urllib.parse import urlparse, urljoin


worker = os.path.dirname(os.path.abspath(__file__))
out_ = os.path.join(worker, "out")
os.makedirs(out_, exist_ok=True)


detail_queue = Queue()
read_queue = Queue()
img_queue = Queue()


def product_detail():
    for i in range(1, 2):
        list_url = f"https://www.jmtt168.com/anime/comics/list/15?page={i}"
        tree = etree.HTML(requests.get(list_url).text)
        blocks = tree.xpath("//div[@class='grid grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-2 md:gap-5 movie-block']/a")
        for block in blocks:
            url = urljoin(
                "https://www.jmtt168.com",
                block.xpath("./@href")[0]
            )
            print(
                "生产detail",
                url
            )
            detail_queue.put(url)

def product_read():
    while True:
        url = detail_queue.get()
        print("消费detail", url)
        tree = etree.HTML(requests.get(url).text)
        url = urljoin(
            "https://www.jmtt168.com",
            tree.xpath("//div[@class='flex flex-wrap gap-3']/a/@href")[0]
        )
        print("生产read", url)
        read_queue.put(url)
        detail_queue.task_done()

def product_img():
    while True:
        # 图库的url
        url = read_queue.get()
        print("消费read", url)
        r = requests.get(url)
        title = re.match("《(.*?)》", etree.HTML(r.text).xpath("//title/text()")[0]).group(1)
        out = os.path.join(out_, title)
        os.makedirs(out, exist_ok=True)
        img_xpath_lists = etree.HTML(r.text).xpath("//div[@class='mx-auto w-full max-w-[808px] border-x border-[var(--jm-border-soft)]']")
        for img_xpath in img_xpath_lists:
            img_url = img_xpath.xpath(".//img/@src")[0]
            print("生产img", img_url)
            img_queue.put({
                "url": img_url,
                "path": os.path.join(out, os.path.basename(urlparse(img_url).path))
            })
        read_queue.task_done()

session = requests.Session()
def consumer():
    while True:
        task = img_queue.get()
        try:
            with open(task["path"], "wb") as f:
                f.write(session.get(task["url"]).content)
            print("消费img", task["url"])
        except Exception as e:
            print("下载失败", task["url"], e)
        finally: # 无论是try还是exception都执行
            img_queue.task_done() 

            
for _ in range(10):
    threading.Thread(
        target=consumer,
        daemon=True
    ).start()
for _ in range(5):
    threading.Thread(
        target=product_img,
        daemon=True
    ).start()
for _ in range(3):
    threading.Thread(
        target=product_read,
        daemon=True
    ).start()
product_detail()

detail_queue.join()
read_queue.join()
img_queue.join()