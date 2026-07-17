import requests

# 指定url及相关参数
# 注意search的api接口，而非浏览器访问页面
url = 'http://www.cpta.com.cn/category/search'

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

param = {
    'keywords': "等级考试",
    '搜索': '搜索'
}

# 发送请求
response = requests.post(url, data=param, headers=header)
response.encoding = response.apparent_encoding

with open("./tmp.html", "w", encoding='utf-8') as f:
    f.write(response.text)