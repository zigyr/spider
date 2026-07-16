import requests
import re
import os
from Crypto.Cipher import AES
from tqdm import tqdm

# ===================== 填写你的 m3u8 地址 =====================
M3U8_URL = "https://hn.bfvvs.com/play/hls/DbDoEQKa/index.m3u8"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://hn.bfvvs.com/"
}
# ==============================================================

# 1. 下载 m3u8
print("[+] 下载 m3u8 索引...")
res = requests.get(M3U8_URL, headers=HEADERS)
m3u8_text = res.text

# 2. 解析 key、IV、ts 列表
key_url = None
ts_list = []
iv = None

lines = m3u8_text.splitlines()
for line in lines:
    if "#EXT-X-KEY" in line:
        # 正则找key_url
        # (.*?)→ 把后面的内容提取出来
        key_uri = re.search(r'URI="(.*?)"', line).group(1)
        # 正则找IV
        # (,|$)→ 直到遇到 逗号， 或者 行尾 停止
        iv_val = re.search(r'IV=(.*?)(,|$)', line).group(1) if "IV=" in line else "0x0000000000000000"
        # 把 IV 从字符串 → 转成计算机能识别的二进制
        iv = bytes.fromhex(iv_val.replace("0x", ""))
        
        # 从字符串右边，按 / 切一刀，分成两部分，丢掉后面那部分，只保留前面的网址基础路径
        base_url = M3U8_URL.rsplit("/", 1)[0]
        key_url = f"{base_url}/{key_uri}"
    
    elif line.startswith("http"):
        ts_list.append(line.strip())

print(f"[+] 共 {len(ts_list)} 个分片")

# 3. 下载密钥
print("[+] 下载解密密钥...")
key = requests.get(key_url, headers=HEADERS).content

# 4. 下载 + 解密 ts 分片
print("[+] 开始下载并解密视频...")
with open("最终视频_可播放.mp4", "wb") as f:
    for url in tqdm(ts_list, desc="下载解密中"):
        try:
            # 下载分片
            ts_data = requests.get(url, headers=HEADERS, timeout=10).content
            
            # 解密
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_ts = cipher.decrypt(ts_data)
            f.write(decrypted_ts)
        except Exception as e:
            print(f"下载失败: {e}")

print("\n✅ 视频已完成！文件名：最终视频_可播放.mp4")