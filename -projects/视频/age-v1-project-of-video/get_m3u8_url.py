
from playwright.async_api import async_playwright


async def get_m3u8_url(target_url):

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        found_m3u8 = None

        async def handle_response(response):

            nonlocal found_m3u8

            url = response.url

            if ".m3u8" in url:
                
                found_m3u8 = url

        page.on("response", handle_response)

        await page.goto(target_url)

        await page.wait_for_timeout(10000)

        await browser.close()

        return found_m3u8