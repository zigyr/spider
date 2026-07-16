import requests
from lxml import etree


url = "https://ks.wangxiao.cn/"

"""
爬取目标：
    - 将所有的一级标题进行爬取
    - 将一级标题对应的二级标题进行爬取
    - 进入到二级标题对应子页面的【每日一练】选项页面中
    - 将每日一练对应的练习题进行数据爬取
"""

headers = {


}

response = requests.get(url, headers=headers)

response.encoding = 'utf-8'

page_text = response.text

# print(page_text)

tree = etree.HTML(page_text)

tags = tree.xpath('//div[@id="banner"]//ul[@class="first-title"]/li')

first_titles = [tag.xpath(".//span/text()") for tag in tags]
send_titless  = [tag.xpath(".//a/text()") for tag in tags]
send_title_hrefss = [tag.xpath(".//a/@href") for tag in tags]

send_data = []
for a, b, c in zip(first_titles, send_titless, send_title_hrefss):

    first_title = [_ for _ in a]
    send_titles = [_ for _ in b]
    send_title_urls = [url + _ for _ in c]
    
    send_data.append(dict(zip(send_titles, send_title_urls)))

# print(send_data)

# 二级标题 + 对应主链接
for _ in send_data:
    for title, url in _.items():
        # print(title, url)
        pass




# 进行每日一练题目的链接爬取
# 一级建造师
# 目标：https://ks.wangxiao.cn/practice/listEveryday?sign=jz1
# 目前：https://ks.wangxiao.cn//TestPaper/list?sign=jz1

from urllib.parse import urlparse, parse_qs

base_url = "https://ks.wangxiao.cn/practice/listEveryday?sign="

in_url = "https://ks.wangxiao.cn//TestPaper/list?sign=jz1"

parsed = urlparse(in_url)

# print(parsed.query)

param = parse_qs(parsed.query)['sign'][0]
# print(param)

out_url = base_url + param

response = requests.get(out_url, headers=headers)
response.encoding = 'utf-8'
page_text = response.text
tree = etree.HTML(page_text)

father_tags = tree.xpath('.//div[@class="test-panel"]/div')

data_titles = [_.xpath('.//li/text()')[1] for _ in father_tags]
data_urls = ["https://ks.wangxiao.cn/" + _.xpath('.//a/@href')[0] for _ in father_tags]

# print(data_titles, data_urls)

second_data = []

for a, b in zip(data_titles, data_urls):
    second_data.append(dict(zip(data_titles, data_urls)))

# print(second_data)





# 第三步了：进入题目页面，进行题目爬取
# https://ks.wangxiao.cn//practice/getQuestion?practiceType=1&sign=jz1&subsign=22c51d8d3ccb4e309a60&day=20260529
# 经过实际考察, 该部分数据属于动态数据类型
# 需要向api:https://ks.wangxiao.cn/practice/listQuestions
# post传入参数{"practiceType":"1","sign":"jz1","subsign":"22c51d8d3ccb4e309a60","day":"20260529"}

url = "https://ks.wangxiao.cn/practice/listQuestions"

in_url = "https://ks.wangxiao.cn//practice/getQuestion?practiceType=1&sign=jz1&subsign=22c51d8d3ccb4e309a60&day=20260529"

parsed = urlparse(in_url)

params = parse_qs(parsed.query)

sign = params['sign']

subsign = params['subsign']

# print(sign, subsign)

data = {
    "practiceType": "1",
    "sign": sign,
    "subsign": subsign,
    "day": "20250621"
}

# https://curlconverter.com/?utm_source=chatgpt.com
# 在其中获取cookie\headers配置
cookies = {
    'UserCookieName': 'pc_391180084',
    'OldUsername2': 'ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D',
    'OldUsername': 'ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D',
    'UserCookieName_': 'pc_391180084',
    'OldUsername2_': 'ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D',
    'OldUsername_': 'ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D',
    'userInfo': '%7B%22userName%22%3A%22pc_391180084%22%2C%22token%22%3A%223c83c401-6a28-420b-89d0-e9c30a9db945%22%2C%22newPlatFormToken%22%3A%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJlNmRkZDc2ZTJjM2RhNDc0ZTM3ZWIyODhjOTgzNGI1NyIsInJuU3RyIjoiNzNZc3pkYlZTU2haTWNIUk5DaWtvdlhLaGlqMm9RT2UiLCJ0ZW1wIjpmYWxzZSwiY2hhbm5lbERldmljZSI6ImFwcF9tb2JpbGVAbnVsbCIsIm1vYmlsZSI6IjE4NTk1OTc3Mjk3In0.QVpAG3g-q3Kr_A6ZKarJs_g6KuPrCbcbODjo_juHjK8%22%2C%22headImg%22%3Anull%2C%22nickName%22%3A%22185****7297%22%2C%22sign%22%3A%22fangchan%22%2C%22isBindingMobile%22%3A%221%22%2C%22isSubPa%22%3A%220%22%2C%22userNameCookies%22%3A%22ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D%22%2C%22passwordCookies%22%3A%22Zjaf4MyWoxw%3D%22%7D',
    'token': '3c83c401-6a28-420b-89d0-e9c30a9db945',
    'NewPlatFormToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJlNmRkZDc2ZTJjM2RhNDc0ZTM3ZWIyODhjOTgzNGI1NyIsInJuU3RyIjoiNzNZc3pkYlZTU2haTWNIUk5DaWtvdlhLaGlqMm9RT2UiLCJ0ZW1wIjpmYWxzZSwiY2hhbm5lbERldmljZSI6ImFwcF9tb2JpbGVAbnVsbCIsIm1vYmlsZSI6IjE4NTk1OTc3Mjk3In0.QVpAG3g-q3Kr_A6ZKarJs_g6KuPrCbcbODjo_juHjK8',
    'OldPassword': 'Zjaf4MyWoxw%3D',
    'OldPassword_': 'Zjaf4MyWoxw%3D',
    'pc_391180084_exam': 'fangchan',
    'acw_tc': '0152e81717808242747803216e9d6e69f0b818e82f2c6c1d69fe0bd737',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'Origin': 'https://ks.wangxiao.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://ks.wangxiao.cn//practice/getQuestion?practiceType=1&sign=jz1&subsign=22c51d8d3ccb4e309a60&day=20260529',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'UserCookieName=pc_391180084; OldUsername2=ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D; OldUsername=ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D; UserCookieName_=pc_391180084; OldUsername2_=ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D; OldUsername_=ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D; userInfo=%7B%22userName%22%3A%22pc_391180084%22%2C%22token%22%3A%223c83c401-6a28-420b-89d0-e9c30a9db945%22%2C%22newPlatFormToken%22%3A%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJlNmRkZDc2ZTJjM2RhNDc0ZTM3ZWIyODhjOTgzNGI1NyIsInJuU3RyIjoiNzNZc3pkYlZTU2haTWNIUk5DaWtvdlhLaGlqMm9RT2UiLCJ0ZW1wIjpmYWxzZSwiY2hhbm5lbERldmljZSI6ImFwcF9tb2JpbGVAbnVsbCIsIm1vYmlsZSI6IjE4NTk1OTc3Mjk3In0.QVpAG3g-q3Kr_A6ZKarJs_g6KuPrCbcbODjo_juHjK8%22%2C%22headImg%22%3Anull%2C%22nickName%22%3A%22185****7297%22%2C%22sign%22%3A%22fangchan%22%2C%22isBindingMobile%22%3A%221%22%2C%22isSubPa%22%3A%220%22%2C%22userNameCookies%22%3A%22ZXUuRQ8bm5Dpu2gomXPqQg%3D%3D%22%2C%22passwordCookies%22%3A%22Zjaf4MyWoxw%3D%22%7D; token=3c83c401-6a28-420b-89d0-e9c30a9db945; NewPlatFormToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJlNmRkZDc2ZTJjM2RhNDc0ZTM3ZWIyODhjOTgzNGI1NyIsInJuU3RyIjoiNzNZc3pkYlZTU2haTWNIUk5DaWtvdlhLaGlqMm9RT2UiLCJ0ZW1wIjpmYWxzZSwiY2hhbm5lbERldmljZSI6ImFwcF9tb2JpbGVAbnVsbCIsIm1vYmlsZSI6IjE4NTk1OTc3Mjk3In0.QVpAG3g-q3Kr_A6ZKarJs_g6KuPrCbcbODjo_juHjK8; OldPassword=Zjaf4MyWoxw%3D; OldPassword_=Zjaf4MyWoxw%3D; pc_391180084_exam=fangchan; acw_tc=0152e81717808242747803216e9d6e69f0b818e82f2c6c1d69fe0bd737',
}


response = requests.post('https://ks.wangxiao.cn/practice/listQuestions', cookies=cookies, headers=headers, json=data)



print(response.request.headers)
print(response.request.body)
