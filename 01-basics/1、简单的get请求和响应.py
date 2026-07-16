import requests

url = 'https://www.baidu.com'
response = requests.get(url)

#响应状态码
print(response.text)
print(response.status_code)
#encoding查看响应内容的编码
print(response.encoding)
#text属性获取报文实体的字符串形式
print(response.text)
#content属性获取报文实体的bytes形式
print(response.content)
#转换成UTF-8形式
#方法一：
print(response.content.decode('utf-8'))
#方法二：
response.encoding='utf-8'
print(response.text)