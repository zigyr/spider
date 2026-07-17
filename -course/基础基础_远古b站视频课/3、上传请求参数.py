import requests
url = 'https://www.baidu.com/s'
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
}
params={
    "wd":"自动化测试"
}
response=requests.get(url,params=params,headers=headers)
with open("text.html", "wb") as tf:
    tf.write(response.content)