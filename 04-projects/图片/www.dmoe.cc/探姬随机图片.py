import requests
import os
import time
import uuid
from datetime import datetime
import hashlib
from pathlib import Path

# 配置项
URL = "http://www.dmoe.cc/random.php"
IMG_DIR = "./04-projects/www.dmoe.cc/images"
TIMEOUT = 10  # 请求超时时间（秒）
RETRY_TIMES = 3  # 请求失败重试次数

# 创建目录
os.makedirs(IMG_DIR, exist_ok=True)


def get_unique_filename(extension="png"):
    """生成唯一的文件名，避免重复"""
    # 方案1：时间戳 + 随机数（可读性好）
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    # random_str = str(uuid.uuid4())[:8]
    # return f"{timestamp}_{random_str}.{extension}"

    # 方案2：UUID（极简，保证唯一）
    return f"{uuid.uuid4()}.{extension}"

    # 方案3：自定义前缀 + 递增数字（需要读取已有文件）
    # prefix = "dmoe_img"
    # existing_files = [f for f in os.listdir(IMG_DIR) if f.startswith(prefix)]
    # max_num = 0
    # for f in existing_files:
    #     try:
    #         num = int(f.split("_")[1].split(".")[0])
    #         max_num = max(max_num, num)
    #     except:
    #         continue
    # return f"{prefix}_{max_num + 1}.{extension}"


def download_image(url, save_path):
    """下载图片，带重试机制"""
    for attempt in range(RETRY_TIMES):
        try:
            # 添加请求头，模拟浏览器访问
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                stream=True  # 流式下载，适合大文件
            )
            response.raise_for_status()  # 抛出HTTP错误

            # 验证响应内容是否为图片
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"警告：响应内容不是图片，Content-Type: {content_type}")
                continue

            # 写入文件
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # 验证文件是否有效
            if os.path.getsize(save_path) < 100:  # 过滤空文件或过小的文件
                os.remove(save_path)
                print(f"警告：文件过小，已删除：{save_path}")
                continue

            return True

        except requests.exceptions.RequestException as e:
            print(f"下载失败（尝试 {attempt + 1}/{RETRY_TIMES}）：{e}")
            time.sleep(1)  # 重试前等待1秒
        except Exception as e:
            print(f"未知错误：{e}")
            if os.path.exists(save_path):
                os.remove(save_path)
            time.sleep(1)

    return False


# 主程序
if __name__ == "__main__":
    # 下载数量
    download_count = 20

    print(f"开始下载 {download_count} 张图片...")

    success_count = 0
    for i in range(download_count):
        # 生成唯一文件名
        img_name = get_unique_filename()
        save_path = os.path.join(IMG_DIR, img_name)

        # 下载图片
        print(f"\n正在下载第 {i + 1}/{download_count} 张图片...")
        if download_image(URL, save_path):
            success_count += 1
            print(f"✅ 成功：{img_name}")
        else:
            print(f"❌ 失败：{img_name}")

        # 避免请求过快
        time.sleep(0.5)

    # 输出结果
    print(f"\n下载完成！")
    print(f"📁 保存目录：{os.path.abspath(IMG_DIR)}")
    print(f"✅ 成功下载：{success_count} 张")
    print(f"❌ 下载失败：{download_count - success_count} 张")