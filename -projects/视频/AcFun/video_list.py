import requests
import os

worker_folder = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(worker_folder, "out")
os.makedirs(output_folder, exist_ok=True) # 如果目录已经存在，不报错，直接继续

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0',
}

params = {
    'type': 'video',
    'keyword': '御姐',
}

r = requests.get('https://www.acfun.cn/search', params=params, headers=headers)

# with open(os.path.join(worker_folder, "1.html"), "w", encoding='utf-8') as f:
#     f.write(r.text)

from lxml import etree

tree = etree.HTML(r.text)

scripts = tree.xpath("//script/text()")

import json

for script in scripts:
    if "pagelet_video" in script:
        obj = json.loads(
            script[script.index("{"):script.rindex("}")+1]
        )
        tree = etree.HTML(obj["html"])
        # 注意这里是一个返回的xpath列表, 需要索引取值, 既是只有一个对象
        video_lists = tree.xpath("//div[@class='video-list']")[0]
        div_tags = video_lists.xpath("//div")
        # for div_tag in div_tags:
        div_tag = div_tags[0]

        titles = div_tag.xpath("//div[@class='video__main__title']/a/text()")
        authors = div_tag.xpath("//span[@class='user-name']/text()")
        images = div_tag.xpath("//div[@class='video__cover']//img/@src")
        durations = div_tag.xpath("//span[@class='video__duration']/text()")
        view_counts = div_tag.xpath("//span[@class='info__view-count']/text()")
        danmaku_counts = div_tag.xpath("//span[@class='info__danmaku-count']/text()")
        create_times = div_tag.xpath("//span[@class='info__create-time']/text()")

        for title, author, image, duration, view_count, danmaku_count, create_time in zip(titles, authors, images, durations, view_counts, danmaku_counts, create_times):
            image = image.split("|")[0]
            r = requests.get(image)
            with open(os.path.join(output_folder, title + ".png"), "wb") as f:
                f.write(r.content)
            print("[ok] ", title, author, duration, view_count, danmaku_count, create_time)