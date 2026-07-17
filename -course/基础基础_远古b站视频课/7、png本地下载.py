import requests

png_url='https://aisearch.cdn.bcebos.com/homepage/dashboard/ai_reading/icon/word.png'

response = requests.get(png_url)

print(response.headers.get("Content-Type"))

with open("baidu.png","wb") as f:
    f.write(response.content)

file={
    "baidu_logol": open("baidu.png","rb")
}

