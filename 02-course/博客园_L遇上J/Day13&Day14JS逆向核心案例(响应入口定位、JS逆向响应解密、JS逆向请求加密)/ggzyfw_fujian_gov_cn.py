import requests
import json

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://ggzyfw.fujian.gov.cn',
    'Referer': 'https://ggzyfw.fujian.gov.cn/business/list/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    'portal-sign': '68afc774bf09d2daf30513328117b36f',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'pageNo': 1,
    'pageSize': 20,
    'total': 0,
    'AREACODE': '',
    'M_PROJECT_TYPE': '',
    'KIND': 'GCJS',
    'GGTYPE': '1',
    'PROTYPE': '',
    'timeType': '6',
    'BeginTime': '2026-01-13 00:00:00',
    'EndTime': '2026-07-13 23:59:59',
    'createTime': '',
    'ts': 1783943368095,
}

response = requests.post('https://ggzyfw.fujian.gov.cn/FwPortalApi/Trade/TradeInfo', headers=headers, json=json_data)

"""
上述部分
每次复制curl(bash)
去`https://curlconverter.com/`
进行更改，保证时间的合法性
"""

data = response.json().get("Data")

import base64
# 将密文数据转换为二进制类型
ecrypted_base64 = base64.b64decode(data)

from Crypto.Cipher import AES
key = "EB444973714E4A40876CE66BE45D5930".encode()
iv = "B5A8904209931867".encode()
aes = AES.new(key, AES.MODE_CBC, iv)
from Crypto.Util.Padding import unpad
data_str = unpad(aes.decrypt(ecrypted_base64), AES.block_size).decode('utf-8')

data_dict = json.loads(data_str)

table_lists = data_dict.get("Table")
for i in table_lists:
    print(i.get("NAME"))