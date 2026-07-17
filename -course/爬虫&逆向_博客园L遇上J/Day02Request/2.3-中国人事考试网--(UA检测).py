import requests

# 指定url及请求参数
url = "http://www.cpta.com.cn/"

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

# 发送请求
response = requests.get(url, headers = header)

# 获取响应数据
page_text = response.text

print(page_text)