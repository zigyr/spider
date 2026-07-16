# import requests

# # 指定url
# url = "https://m.media-amazon.com/images/I/71ejlJ4yX1L._SY522_.jpg"

# # 发送请求
# response = requests.get(url)

# # 获取响应数据
# page_text = response.content

# # 本地存储
# with open("./MikamiYua.png", "wb") as f:
#     f.write(page_text)

from urllib.request import urlretrieve

url = "https://m.media-amazon.com/images/I/71ejlJ4yX1L._SY522_.jpg"

urlretrieve(url, "./MikamiYua.png")