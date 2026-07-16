import requests
import os
from lxml import etree
import time
import random

def down_side(url, path):
    response = requests.get(url)
    response.encoding = 'utf-8'
    tree = etree.HTML(response.text)

    div_tags = tree.xpath("//*[@id='post_content']//img/@data-original")

    for i, div_tag in enumerate(div_tags):
        rand_str = str(random.randint(1000, 9999))
        time_str = time.strftime("%Y%m%d_%H%M%S")
        img_url = "https:" + div_tag
        title = f"{time_str}_{rand_str}.png"
        try:
            with open(os.path.join(path, f"{time_str}_{rand_str}.png"), "wb") as f:
                f.write(requests.get(img_url).content)
                print(title, ":下载完成!!!")
        except:
            print(title, "下载失败!!!")

url = "https://wyfsm.com/douyinweimi_1/"

response = requests.get(url)

response.encoding = 'utf-8'

tree = etree.HTML(response.text)

li_tags = tree.xpath('//*[@id="post_container"]/div/li')

for li_tag in li_tags:

    a_tag = li_tag.xpath('./div[@class="thumbnail"]/a')[0]

    src = a_tag.xpath('./@href')[0]
    url = "https://wyfsm.com" + src
    title = a_tag.xpath('./@title')[0].split(" ")[1]
    path = f"F:\\code_practice\\code\\python\\00-爬虫\\爬虫&逆向\\Day03数据解析\\img\\{title}"

    os.makedirs(path, exist_ok=True)

    down_side(url, path)
