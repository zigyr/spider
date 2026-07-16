import requests

url='https://www.baidu.com'
response=requests.get(url)

for key in response.headers.keys():
    print(f"{key}:{response.headers[key]}")