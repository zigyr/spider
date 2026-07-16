import requests
from lxml import etree
from pathlib import Path
from urllib.parse import urljoin, quote
import time
import logging
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

BASE_URL = "https://www.ibbs.pro"

SAVE_ROOT = Path("04-projects/www.ibbs.pro/images")

headers = {
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

session = requests.Session()
session.headers.update(headers)

# =========================
# 工具函数
# =========================
def download_image(
    img_url: str,
    save_path: Path
) -> bool:
    """
    下载单张图片并保存到指定路径。

    Args:
        image_url (str): 图片的完整 URL。
        save_path (Path): 图片保存路径。

    Returns:
        bool:
            True  下载成功。
            False 下载失败。
    """
    try:
        r = session.get(
            img_url,
            timeout=10
        )

        # 检查状态码，如果出错则抛出异常
        r.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(r.content)

        return True

    except Exception as error:

        logging.error("下载失败: %s", img_url)

        return False


# =========================
# 图库页面解析
# =========================
def download_gallery(
        gallery_url: str,
        gallery_title: str
) -> int:
    """
    下载指定图库中的所有图片。

    进入图库页面，解析图片链接，创建保存目录，
    并依次下载所有图片。

    Args:
        gallery_url (str): 图库详情页 URL。
        gallery_title (str): 图库标题。

    Returns:
        int: 成功下载的图片数量。
    """

    print("进入图库:", gallery_title)

    r = session.get(
        gallery_url,
        timeout=10
    )

    tree = etree.HTML(r.text)

    img_urls = (
        tree.xpath('//div[contains(@class,"text-wrap")]//img/@src')
        +
        tree.xpath('//div[contains(@class,"text-break")]//img/@src')
    )

    save_folder = (
        SAVE_ROOT
        /
        gallery_title
    )
    save_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"发现图片: {len(img_urls)} 张"
    )

    
    tasks = []

    for index, img in enumerate(img_urls,1):

        img_url = urljoin(
            BASE_URL,
            img
        )
        save_path = (
            save_folder
            /
            f"{index}.jpg"
        )

        # 已存在跳过
        if save_path.exists():
            tqdm.write(f"[跳过] {index}/{len(img_urls)}")
            continue

        tasks.append(
            (img_url, save_path)
        )

    success_count = 0

    with ThreadPoolExecutor (max_workers=16) as executor:
        futures = [
            executor.submit(
                download_image,
                img_url,
                save_path
            )
            for img_url, save_path in tasks
        ]

        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc=gallery_title,
            unit="张"
        ):
            if future.result():
                success_count += 1


    return success_count

# =========================
# 搜索页面爬取
# =========================
def search_gallery(
    keyword: str
) -> list[tuple[str, str]]:
    """
    根据关键词搜索图库。

    自动遍历所有搜索结果页面，收集图库链接及标题。

    Args:
        keyword (str): 搜索关键词。

    Returns:
        list[tuple[str, str]]:
            图库列表，每个元素格式为：

            (
                gallery_url,
                gallery_title
            )
    """
    next_url = (
        f"{BASE_URL}/searchthread?"
        f"s={quote(keyword)}"
    )

    gallery_list = []
    
    while next_url:

        print("正在解析:", next_url)
        
        r = session.get(next_url)

        tree = etree.HTML(r.text)

        # 这个xpath很强
        urls = tree.xpath('//a[@title]/@href')
        titles = tree.xpath('//a[@title]/@title')

        for u, t in zip(urls, titles):
            gallery_list.append(
                (urljoin(BASE_URL, u), t)
            )

        # 找下一页
        next_page = tree.xpath('//a[contains(text(),"下一页")]/@href')

        if next_page:
            next_url = urljoin(BASE_URL, next_page[0])
        else:
            next_url = None
    
    return gallery_list

# =========================
# 主程序
# =========================
def main():

    start_time = time.time()

    print("="*50)
    print("       https://www.ibbs.pro网站图库下载器")
    print("="*50)

    keyword = input("请输入搜索关键词: ")

    galleries = search_gallery(keyword)

    if not galleries:
        print("没有找到图库")
        return

    print(f"共发现图库: {len(galleries)}")

    limit = int(input("请输入下载图库数量: "))

    limit = min(limit, len(galleries))

    total_gallery = 0
    total_image = 0

    # enumerate第二个参数表示起始编号
    for index, (url, title) in enumerate(galleries[:limit], 1):
        print(
            "\n"
            +
            "="*40
        )
        print(
            f"进度 {index}/{limit}"
        )
        count = download_gallery(
            url,
            title
        )
        total_image += count
        total_gallery += 1

    cost = time.time()-start_time

    print(
        "="*40,
        "下载完成",
        "="*40
    )

    print(
        f"完成图库: {total_gallery} 个"
    )

    print(
        f"下载图片: {total_image} 张"
    )

    print(
        f"保存位置: {SAVE_ROOT.absolute()}"
    )

    print(
        f"耗时: {cost:.2f} 秒"
    )


if __name__=="__main__":
    main()