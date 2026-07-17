import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
url = 'http://www.cip.cc/'

# proxies={'http': '111.72.197.78:3828'} 代理类型
# page_text = requests.get(url, headers=headers, proxies={'http': '111.72.197.78:3828'}).text
page_text = requests.get(url, headers=headers).text

tree = etree.HTML(page_text)
text = tree.xpath('/html/body/div/div/div[3]/pre/text()')[0]
print(text)
"""
代理类型：proxies={'http': '111.72.197.78:3828'}中具体是https还是http取决于访问的url中是https还是http
如果请求的url是https代理类型就需要是https:ip+端口,如果请求的url是http代理类型就需要是http:ip+端口
"""