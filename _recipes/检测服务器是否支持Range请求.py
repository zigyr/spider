"""
原项目 -projects/视频/cn.xgroovy.com/
功能   检测服务器是否支持 HTTP Range 请求
"""

from lxml import etree
import time
import requests

url = "https://cn.xgroovy.com/videos/732142/slim-petite-teen-fingers-her-tiny-bald-pussy-gets-creamy-orgasm-in-hot-female-pov/"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": url,
    "Range": "bytes=0-0"
}

session = requests.session()
session.headers.update(headers)

r = session.get(url)

tree = etree.HTML(r.text)

video_url = tree.xpath('//*[@id="video_source_4"]/@src')[0]

r = session.get(
    video_url,
    stream=True,
    allow_redirects=True
)

# 206 Partial Content
# 这是 HTTP Range 生效 的标志。
print(r.status_code)
print(r.headers.get("Content-Range"))
print(r.headers.get("Accept-Ranges"))
print(next(r.iter_content(1)))