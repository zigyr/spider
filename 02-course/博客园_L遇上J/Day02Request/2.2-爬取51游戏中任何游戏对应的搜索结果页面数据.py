
import requests

# 指定url及相关参数
url = "https://game.51.com/search/action/game/"

game_title = "王者荣耀"
param = {
    'q': game_title
}

# 发送请求
response = requests.get(url, params=param)

# response.encoding = 'utf-8'

print(response.text)

