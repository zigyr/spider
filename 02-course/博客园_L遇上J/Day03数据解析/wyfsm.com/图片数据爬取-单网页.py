import requests
from lxml import etree
import os

url = "https://wyfsm.com/kMaI8W.html"


response = requests.get(url)

response.encoding = 'utf-8'

out_folder = r"F:\code_practice\code\python\00-爬虫\爬虫&逆向\Day03数据解析\img"

tree = etree.HTML(response.text)

div_tags = tree.xpath("//*[@id='post_content']//img/@data-original")

for i, div_tag in enumerate(div_tags):
    img_url = "https:" + div_tag
    with open(os.path.join(out_folder, str(i)+".png"), "wb") as f:
        f.write(requests.get(img_url).content)
    print(i, ":下载完成!!!")