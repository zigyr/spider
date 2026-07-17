import os
import re
import time
import requests

from dataclasses import dataclass
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from concurrent.futures import as_completed, ThreadPoolExecutor

M3U8_URL = "https://hn.bfvvs.com/play/hls/penkJg7a/index.m3u8"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36"
    ),
    "Referer": "https://hn.bfvvs.com/"
}


@dataclass
class VideoInfo:
    key: bytes
    iv: bytes
    ts_list: list


def get_m3u8_text():
    response = requests.get(M3U8_URL, headers=HEADERS)
    return response.text


def parse_m3u8(m3u8_text):

    ts_list = []
    key = None
    iv = None

    for line in m3u8_text.splitlines():

        line = line.strip()

        if "#EXT-X-KEY" in line:

            key_uri = re.search(r'URI="(.*?)"', line).group(1)

            key_url = os.path.dirname(M3U8_URL) + "/" + key_uri

            key = requests.get(key_url, headers=HEADERS).content

            iv_match = re.search(r"IV=(.*?)(,|$)", line)

            if iv_match:
                iv_hex = iv_match.group(1).replace("0x", "")
            else:
                iv_hex = "0000000000000000"

            iv = bytes.fromhex(iv_hex)

        elif line.startswith("http"):
            ts_list.append(line)

    return VideoInfo(
        key=key,
        iv=iv,
        ts_list=ts_list
    )


def decrypt_ts(ts_data, video_info):

    block_size = AES.block_size
    pad_len = (block_size - len(ts_data) % block_size) % block_size
    ts_data += bytes([pad_len]) * pad_len

    aes = AES.new(
        video_info.key,
        AES.MODE_CBC,
        video_info.iv
    )

    decrypted_data = aes.decrypt(ts_data)

    try:
        decrypted_data = unpad(
            decrypted_data,
            AES.block_size
        )
    except:
        pass

    return decrypted_data

def download_ts(index, ts_url):

    try:

        ts_data = requests.get(
            ts_url,
            headers=HEADERS
        ).content

        return index, ts_data

    except Exception as e:

        return index, None


pool = ThreadPoolExecutor(max_workers=30)

def download(video_info):

    futures = []

    for index, ts in enumerate(video_info.ts_list):
        
        future = pool.submit(
            download_ts,
            index,
            ts
        )

        futures.append(future)

    results = {}

    for future in as_completed(futures):
        
        index, ts_data = future.result()

        results[index] = ts_data

        print(f"[+] 切片 {index} 下载完成")
    return results

cou = 0

def merge_ts(results, video_info):

    global cou

    with open("ZZFLL.mp4", "wb") as f:

        for index in sorted(results):

            if results[index]:
                
                cou += 1

                decrypted_data = decrypt_ts(
                    results[index],
                    video_info
                )

                f.write(decrypted_data)


def main():

    start_time = time.time()

    print("[-] 开始获取 m3u8")

    m3u8_text = get_m3u8_text()

    print("[+] m3u8 获取成功")

    print("[-] 开始解析 m3u8")

    video_info = parse_m3u8(m3u8_text)

    print("[+] m3u8 解析完成")

    print(
        f"[-] 开始下载\n"
        f"共 {len(video_info.ts_list)} 个切片"
    )

    results = download(video_info)

    print("[+] 开始合并")

    merge_ts(results, video_info)



    end_time = time.time()

    print(
        f"[+] 总耗时: "
        f"{end_time - start_time:.4f} s"
    )

    print(
        f"[+] 下载成功率: {cou / len(results) * 100:.2f}%"
    )


if __name__ == "__main__":
    main()

"""20threadpoolexecutor
[+] 下完整率: 99.32%
[+] 总耗时: 100.5094 s
"""

"""30threadpoolexecutor
[+] 下完整率: 68.71%
[+] 总耗时: 63.4907 s
"""

"""40threadpoolexecutor
[+] 下完整率: 83.67%
[+] 总耗时: 48.6294 s
"""