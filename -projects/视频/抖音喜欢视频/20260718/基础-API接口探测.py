"""
Date: 2026-07-18
Author: zigyr
"""
import json
import requests

cookies = {
    'sid_guard': '2396842c36309e1898616cfd41f16ecb%7C1783143834%7C5184000%7CWed%2C+02-Sep-2026+05%3A43%3A54+GMT',
    'ttwid': '1%7C8kecg4UAA3FMw_hlCgjMDKEGKgrjopaSW-xam89EiT8%7C1784355005%7C0205c28397847f5c9df09442a93deeb5e37665a323dc3a20a90f7c641ba1955f',
}

# 固定值
headers = {
    'referer': 'https://www.douyin.com/',
}

# 固定值
params = {
    'aid': '6383',
}

response = requests.get('https://www-hj.douyin.com/aweme/v1/web/aweme/favorite/', params=params, cookies=cookies, headers=headers)

data = response.json()

print(data.keys())
print(data.get("status_code"))
print(data.get("status_msg"))
print(len(data.get("aweme_list", [])))

with open("3.json", "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)