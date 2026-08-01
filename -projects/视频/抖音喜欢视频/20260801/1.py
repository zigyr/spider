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
while True:
    packet = tab.listen.wait(timeout=10)
    if packet:
        global data 
        data = packet.response.body
        break

for aweme_list in data["aweme_list"]:
    title = aweme_list.get("desc")
    url = aweme_list["video"]["play_addr"]["url_list"][0]
    print(title, url)