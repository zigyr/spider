
import asyncio
import aiohttp
import aiofiles
import os
import re
import time

from urllib.parse import urljoin
from Crypto.Cipher import AES
from tqdm import tqdm


class M3U8Downloader:

    def __init__(
            self,
            headers=None,
            max_tasks=50,
            timeout=20,
            retry=3,
            temp_dir="temp_ts"
    ):

        self.headers = headers or {
            "User-Agent": "Mozilla/5.0"
        }

        self.max_tasks = max_tasks
        self.timeout = timeout
        self.retry = retry
        self.temp_dir = temp_dir

        os.makedirs(temp_dir, exist_ok=True)

    # ====================================
    # 解析 m3u8
    # ====================================
    async def parse_m3u8(self, session, m3u8_url):

        async with session.get(m3u8_url) as resp:
            text = await resp.text()

        lines = text.splitlines()

        ts_list = []

        key = None
        iv = bytes(16)

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # AES KEY
            if "#EXT-X-KEY" in line:

                key_uri = re.search(
                    r'URI="(.*?)"',
                    line
                ).group(1)

                iv_match = re.search(
                    r'IV=(.*?)(,|$)',
                    line
                )

                if iv_match:
                    iv_hex = iv_match.group(1).replace("0x", "")
                    iv = bytes.fromhex(iv_hex.zfill(32))

                key_url = urljoin(m3u8_url, key_uri)

                async with session.get(key_url) as key_resp:
                    key = await key_resp.read()

            # TS
            elif not line.startswith("#"):

                ts_url = urljoin(m3u8_url, line)

                ts_list.append(ts_url)

        return ts_list, key, iv

    # ====================================
    # 下载单个 ts
    # ====================================
    async def download_segment(
            self,
            session,
            ts_url,
            index,
            key,
            iv,
            semaphore,
            pbar
    ):

        ts_path = os.path.join(
            self.temp_dir,
            f"{index}.ts"
        )

        # 已存在 -> 断点续传
        if os.path.exists(ts_path):
            pbar.update(1)
            return

        async with semaphore:

            for attempt in range(self.retry):

                try:

                    async with session.get(ts_url) as resp:

                        if resp.status != 200:
                            raise Exception(
                                f"HTTP {resp.status}"
                            )

                        data = await resp.read()

                        # AES 解密
                        if key:

                            cipher = AES.new(
                                key,
                                AES.MODE_CBC,
                                iv
                            )

                            data = cipher.decrypt(data)

                        async with aiofiles.open(
                                ts_path,
                                "wb"
                        ) as f:

                            await f.write(data)

                        pbar.update(1)

                        return

                except Exception as e:

                    if attempt == self.retry - 1:

                        print(
                            f"\n❌ 分片失败: {index}"
                        )

                    await asyncio.sleep(1)

    # ====================================
    # 合并 ts
    # ====================================
    async def merge_segments(
            self,
            output_file,
            total
    ):

        async with aiofiles.open(
                output_file,
                "wb"
        ) as outfile:

            for i in range(total):

                ts_path = os.path.join(
                    self.temp_dir,
                    f"{i}.ts"
                )

                if not os.path.exists(ts_path):
                    continue

                async with aiofiles.open(
                        ts_path,
                        "rb"
                ) as infile:

                    data = await infile.read()

                    await outfile.write(data)

        print(f"\n✅ 合并完成: {output_file}")

    # ====================================
    # 主下载 API
    # ====================================
    async def download(
            self,
            m3u8_url,
            output_file
    ):

        start_time = time.time()

        connector = aiohttp.TCPConnector(
            limit=100,
            ssl=False
        )

        timeout = aiohttp.ClientTimeout(
            total=self.timeout
        )

        async with aiohttp.ClientSession(
                headers=self.headers,
                connector=connector,
                timeout=timeout
        ) as session:

            print("[+] 解析 m3u8...")

            ts_list, key, iv = await self.parse_m3u8(
                session,
                m3u8_url
            )

            print(f"[+] ts数量: {len(ts_list)}")

            semaphore = asyncio.Semaphore(
                self.max_tasks
            )

            pbar = tqdm(
                total=len(ts_list),
                desc="下载进度",
                unit="ts",
                ncols=100
            )

            tasks = []

            for index, ts_url in enumerate(ts_list):

                task = asyncio.create_task(

                    self.download_segment(
                        session,
                        ts_url,
                        index,
                        key,
                        iv,
                        semaphore,
                        pbar
                    )
                )

                tasks.append(task)

            await asyncio.gather(*tasks)

            pbar.close()

            print("[+] 开始合并视频...")

            await self.merge_segments(
                output_file,
                len(ts_list)
            )

            cost = time.time() - start_time

            print(
                f"\n✅ 总耗时: {cost:.2f}s"
            )


# ====================================
# 外部调用 API
# ====================================
async def main():

    target_url = input("请输入视频的链接(age动漫)：")

    # ===========================================
    # 获取视频资源信息
    from get_detail_info import get_detail_info
    anime_title, episode_num, file_name= get_detail_info(target_url)
    print(f"[+] 动漫标题: {anime_title}")
    print(f"[+] 集数: 第{episode_num}集")
    print(f"[+] 预计生成的文件名: {file_name}")
    
    # ===========================================
    # 解析m3u8_url
    from get_m3u8_url import get_m3u8_url
    print("[+] 正在解析m3u8_url")
    m3u8_url = await get_m3u8_url(target_url)
    print(f"[+] 成功解析m3u8_url: {m3u8_url}")


    downloader = M3U8Downloader(

        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://hn.bfvvs.com/"
        },

        max_tasks=80,
        retry=5
    )

    await downloader.download(
        f"{m3u8_url}",
        f"{file_name}"
    )


if __name__ == "__main__":

    asyncio.run(main())

