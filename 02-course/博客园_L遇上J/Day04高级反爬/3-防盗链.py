# 网页请求爬取
import requests
from lxml import etree

url = "http://slide.eladies.sina.com.cn/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    'referer': 'http://slide.eladies.sina.com.cn/'
}

response = requests.get(url, headers=headers)

response.encoding = 'gbk'

page_text = response.text

# print(page_text)

tree = etree.HTML(page_text)

img_lists = tree.xpath('//*[@id="eData"]/dl/dd[4]/text()')
# print(img_lists)

for img_tag in img_lists:
    # print(img_tag)
    pass

# api调用爬取
import requests

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://slide.eladies.sina.com.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}
cookies = {
    "UOR": ",blog.sina.com.cn,",
    "SINAGLOBAL": "113.201.142.195_1780797955.58639",
    "Apache": "113.201.142.195_1780797955.58640",
    "lxlrttp": "1578733570",
    "ULV": "1780798016413:2:2:2:113.201.142.195_1780797955.58640:1780797955098",
    "U_TRS1": "0000004b.e95860ee.6a24d240.a07b4343",
    "U_TRS2": "0000004b.e96060ee.6a24d240.a47a737c"
}
url = "http://api.slide.news.sina.com.cn/interface/api_album.php"
params = {
    "activity_size": "198_132",
    "size": "img",
    "ch_id": "3",
    "page": "1",
    "num": "16",
    "_": "1780799710375"
}
response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)


page_text = response.json()

# content_type = response.headers.get('Content-Type')

# print(page_text)

items = page_text['data']

for item in items:
    print(item['img_url'])