from DrissionPage import Chromium, ChromiumOptions
import json
import os

worker_folder = os.path.dirname(os.path.abspath(__file__))
out_ = os.path.join(worker_folder, "out")
os.makedirs(out_, exist_ok=True)

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



def save_video(data):
    with open(os.path.join(worker_folder, "video.json"), "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    
all_video = []
while True: 
    packet = tab.listen.wait(timeout=10) 
    data = packet.response.body

    for item in data["aweme_list"]: 
        video = {
            "title": item["desc"],
            "url": item["video"]["play_addr"]["url_list"][0],
            "id": item["aweme_id"]
        }
        all_video.append(video)
        if len(all_video) % 50 == 0:
            save_video(all_video)
            print("已保存:", len(all_video))
    print( "当前数量:", len(all_video) )
    if data["has_more"] == 0:
        break

with open(os.path.join(out_, "video.json"), "w", encoding='utf-8') as f:
    json.dump(all_video, f, ensure_ascii=False, indent=4)