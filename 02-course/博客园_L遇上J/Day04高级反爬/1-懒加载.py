import requests
from lxml import etree
import os

url = "https://sc.chinaz.com/tupian/meinvxiezhen.html"

response = requests.get(url)

response.encoding = "utf-8"

tree = etree.HTML(response.text)

div_tags = tree.xpath("/html/body/div[3]/div[2]/div/img")

out_folder = r"F:\code_practice\code\python\00-爬虫\爬虫&逆向\Day04高级反爬\img"

for div_tag in div_tags:

    alt_tag = div_tag.xpath("./@alt")[0]
    # 懒加载：data-original伪地址，使用懒加载的方式保留图片的地址
    img_url = "https://" + div_tag.xpath("./@data-original")[0][2:]
    
    res = requests.get(img_url)

    with open(os.path.join(out_folder, alt_tag+".png"), "wb") as f:
        f.write(res.content)
    
    print(alt_tag, ":保存成功!!!")

