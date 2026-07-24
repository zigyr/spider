import requests
import os

worker_folder = os.path.dirname(os.path.abspath(__file__))

import requests

cookies = {
    '_did': 'web_863913283C23BD4D',
    'lsv_js_player_v2_main': 'ca85g8',
    'csrfToken': '0BtjY2Mska9KGJTOMdGz8-Px',
    'cur_req_id': '583990853EF47169_self_2d45c537a4f93b4689463857c3114dd1',
    'cur_group_id': '583990853EF47169_self_2d45c537a4f93b4689463857c3114dd1_0',
    'webp_supported': '%7B%22lossy%22%3Atrue%2C%22lossless%22%3Atrue%2C%22alpha%22%3Atrue%2C%22animation%22%3Atrue%7D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.acfun.cn/',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Microsoft Edge";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0',
    # 'cookie': '_did=web_863913283C23BD4D; lsv_js_player_v2_main=ca85g8; csrfToken=0BtjY2Mska9KGJTOMdGz8-Px; cur_req_id=583990853EF47169_self_2d45c537a4f93b4689463857c3114dd1; cur_group_id=583990853EF47169_self_2d45c537a4f93b4689463857c3114dd1_0; webp_supported=%7B%22lossy%22%3Atrue%2C%22lossless%22%3Atrue%2C%22alpha%22%3Atrue%2C%22animation%22%3Atrue%7D',
}

params = {
    'type': 'video',
    'keyword': '御姐',
}

r = requests.get('https://www.acfun.cn/search', params=params, cookies=cookies, headers=headers)

# with open(os.path.join(worker_folder, "1.html"), "w", encoding='utf-8') as f:
#     f.write(r.text)

from lxml import etree

tree = etree.HTML(r.text)

scripts = tree.xpath("//script/text()")

import json

for script in scripts:
    if "bigPipe.onPageletArrive" in script:
        # 切片提取json对象
        # 函数名(json对象)
        # rindex: 找到最后的
        # index:  找到最前的
        obj = json.loads(
            script[script.index("{"):
            script.rindex("}")+1]
        )
        id = obj["id"].split("_")[-1]
        print(id)

        sign = id + "-list"
        tree = etree.HTML(obj["html"])
