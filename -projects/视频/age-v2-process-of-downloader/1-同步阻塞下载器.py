import os
import re
import time
import requests

from dataclasses import dataclass
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

"""
说白了，就是普通下载的意思
"""
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


def download_video(video_info):

    success_count = 0

    with open("ZSFLL.mp4", "wb") as file:

        for index, ts_url in enumerate(video_info.ts_list):

            try:

                ts_data = requests.get(
                    ts_url,
                    headers=HEADERS
                ).content

                decrypted_data = decrypt_ts(
                    ts_data,
                    video_info
                )

                file.write(decrypted_data)

                print(f"[+] 切片 {index} 下载成功")

                success_count += 1

            except Exception as e:

                print(
                    f"[-] 切片 {index} 下载失败: {e}"
                )

    rate = success_count / len(video_info.ts_list) * 100

    print(f"[+] 下载成功率: {rate:.2f}%")


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

    download_video(video_info)

    end_time = time.time()

    print(
        f"[+] 总耗时: "
        f"{end_time - start_time:.4f} s"
    )


if __name__ == "__main__":
    main()

"""request
[+] 下载成功率: 97.28%
[+] 总耗时: 445.8008 s
"""