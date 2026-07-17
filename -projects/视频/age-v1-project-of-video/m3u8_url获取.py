from playwright.sync_api import sync_playwright

target_url = "https://www.agedm.io/play/20230207/4/2"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )

    page = browser.new_page()

    found = set()

    def handle_response(response):
        url = response.url

        if ".m3u8" in url:
            if url not in found:
                found.add(url)
                pass


    page.on("response", handle_response)

    page.goto(target_url)

    # 等待播放器加载
    page.wait_for_timeout(15000)

    browser.close()

m3u8_url = list(found)[0]

print("[+]开始解析m3u8_url")

print(f"[+]成功解析m3u8_url: {m3u8_url}")