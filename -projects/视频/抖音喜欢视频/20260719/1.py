import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.douyin.com',
    'Pragma': 'no-cache',
    'Range': 'bytes=0-',
    'Referer': 'https://www.douyin.com/',
    'Sec-Fetch-Dest': 'video',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Microsoft Edge";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'a': '6383',
    'ch': '4',
    'cr': '3',
    'dr': '0',
    'lr': 'all',
    'cd': '0|0|0|3',
    'cv': '1',
    'br': '1566',
    'bt': '1566',
    'cs': '0',
    'ds': '4',
    'ft': 'pEaFx4hZffPdp8~Sa13NvAq-antLjrKvn6auRka22u9WejVhWL6',
    'mime_type': 'video_mp4',
    'qs': '0',
    'rc': 'NjVmNGY7Ozc6O2c3NzU4PEBpM2l1bHY5cmh3PDMzbGkzNUBfMjEtXi4yXmIxYTQwLl5iYSNoamtgMmQ0NS5hLS1kLTVzcw==',
    'btag': '80000e00010000',
    'cquery': '100x_100z_100o_101r_100B',
    'dy_q': '1784716118',
    'feature_id': '37f92ebd2877ae8e7eba995d406c5150',
    'l': '202607221828381D6C961FF7689F9611A6',
    '__vid': '7657204011867717489',
}

response = requests.get(
    'https://v11-weba.douyinvod.com/16944263bccbfbdadf4da86a2d469b20/6a60c59a/video/tos/cn/tos-cn-ve-15c000-ce/o8rPADHE9oVf7QhoFwQ9rE8QIAyqe4DAx4bEFB/',
    params=params,
    headers=headers,
)

import os

root_dir = os.path.dirname(os.path.abspath(__file__))
outp_dir = os.path.join(root_dir, "out")

with open(os.path.join(outp_dir, "1.mp4"), "wb") as f:
    f.write(response.content)