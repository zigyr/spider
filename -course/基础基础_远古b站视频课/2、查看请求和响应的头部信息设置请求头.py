import requests
url = 'https://www.baidu.com'
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
}
response=requests.get(url,headers=headers)
#响应头部信息
print(response.headers)
print(type(response.headers))
#请求头部信息
print(response.request.headers)
print(type(response.request.headers))
#查看网页信息
#方法一
response.encoding='utf-8'
print(response.text)
#方法二
with open('text1.html', 'wb') as tf:
    tf.write(response.content)

with open('text2.html', 'wb') as tf:
    tf.write(response.text.encode('utf8'))

response.encoding='utf-8'
with open('text3.html', 'w', encoding='utf-8') as tf:
    tf.write(response.text)