
import requests


url = "https://www.eastmoney.com/"

response = requests.get(url)

# 查看响应状态码
print(response.status_code)

# 中文乱码解决
response.encoding = response.apparent_encoding
response.encoding = 'utf-8'
print(response.text)