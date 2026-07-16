import requests
from bs4 import BeautifulSoup

url = "https://bixuejian.5000yan.com/"

response = requests.get(url)

response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'lxml')

a_tags = soup.select(".mx-auto li")

out = r"F:\code_practice\code\python\00-爬虫\爬虫&逆向\Day03数据解析\碧血剑.txt"

fp = open(out, "w", encoding='utf-8')

for a_tag in a_tags:

    page_title = a_tag.text

    page_url = a_tag.find('a')['href']
    content_res = requests.get(page_url)
    content_res.encoding = 'utf-8'
    soup = BeautifulSoup(content_res.text, 'lxml')
    content = soup.find("div", class_='grap').text

    fp.write(page_title + ":" + content + '\n')

    print(page_title + ":章节爬取保存成功！")

fp.close()