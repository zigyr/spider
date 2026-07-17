import requests

from lxml import etree


url = "https://www.aqistudy.cn/historydata/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# verify=False可以兼容请求url时出现的"不安全"的错误
# response = requests.get(url, headers=headers, verify=False)
response = requests.get(url, headers=headers)

response.encoding = 'utf-8'

page_text = response.text

# print(page_text)

tree = etree.HTML(page_text)

# 管道符：ex1 | ex2  只要是符合 ex1 或 ex2 的都会被解析出来
a_list = tree.xpath(
    '/html/body/div[3]/div/div[1]/div[1]/div[2]//a | /html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]//a'
)
for a_tag in a_list:
    title = a_tag.xpath('./text()')[0]
    print(title)

    
# # 解析热门城市
# a_list = tree.xpath('/html/body/div[3]/div/div[1]/div[1]/div[2]//a')
# for a_tag in a_list:
#     title = a_tag.xpath('./text()')[0]
#     print(title)

# print('\n')

# # 解析全部城市
# a_list = tree.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]//a')
# for a_tag in a_list:
#     title = a_tag.xpath('./text()')[0]
#     print(title)