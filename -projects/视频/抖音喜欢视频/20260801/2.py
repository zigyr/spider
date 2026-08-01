from DrissionPage import Chromium, ChromiumOptions

co = ChromiumOptions()
co.set_browser_path(
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)
co.set_user_data_path(
    r"E:\EdgeProfile"
)
browser = Chromium(co)
tab = browser.latest_tab


tab.listen.start("v1/web/aweme/post/")
tab.get("https://www.douyin.com/user/MS4wLjABAAAAx4riwMpMmsQqVWzRrmgoGfoMHbB7SeBLXbgiPBzbuMc?from_tab_name=main")


all_video = []
while True: 
    packet = tab.listen.wait(timeout=10) 
    if packet: 
        data = packet.response.body 
        for item in data["aweme_list"]: 
            video = {
                "title": item["desc"],
                "url": item["video"]["play_addr"]["url_list"][0],
                "id": item["aweme_id"]
            }
            all_video.append(video)
    print( "当前数量:", len(all_video) )
    if data["has_more"] == 0:
        break

print(
    [(v["title"], v["url"]) for v in all_video]
)
"""
手动翻页
可实现所有视频信息的获取
包括视频url
"""