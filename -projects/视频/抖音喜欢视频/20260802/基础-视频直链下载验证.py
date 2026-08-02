import requests

url = "https://v11-weba.douyinvod.com/a552778b1a249eb7ca32524b31962b8c/6a6eb65a/video/tos/cn/tos-cn-ve-15c000-ce/okIASiouiCBZERBnEfFMWeQwi7MiYE9MTsfA9v/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=676&bt=676&cs=0&ds=3&ft=4TMWc6DhppftDFLB.Co.C_fauVq0InQ_XPpc6Bd-IRK1HQdHDD~q69Xh~.4PuusZ.&mime_type=video_mp4&qs=0&rc=ZTxmODw4OGgzZ2VpOjhmZEBpM3M4O3c5cjk1MzMzbGkzNEA1X2IwYWJhNWAxLTUwYS0zYSNgM2ZrMmRjczZhLS1kLWJzcw%3D%3D&btag=80000e00010000&cquery=101r_100B_100x_100z_100o&dy_q=1785629722&feature_id=fea919893f650a8c49286568590446ef&l=20260802081522F7447B80AC9386850A62"

r = requests.get(url, stream=True)

with open("1.mp4", "wb") as f:
    for chunk in r.iter_content(1024*1024): # 这是results的写法, aiohttp中没有这个
        if chunk:
            f.write(chunk)

# 经过验证视频的下载不需要什么头