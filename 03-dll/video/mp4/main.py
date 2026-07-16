import requests


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "i",
    "range": "bytes=0-",
    "referer": "https://cn.xgroovy.com/",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\"",
    "sec-ch-ua-full-version": "\"150.0.7871.101\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"10.0.0\"",
    "sec-fetch-dest": "video",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "sec-fetch-storage-access": "active",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}

url = "https://ip179698702.ahcdn.com/key=vLLqXbNmD9Wu2p8S7CxKLQ,s=,end=1783699189,limit=2/data=NA720P/state=alEIDsfg/buffer=396000/speed=132000/reftag=0194637682/origin=280760249/680000/680643/680643.mp4"

def download(url, filename):

    r = requests.get(
        url,
        stream=True
    )

    total = int(
        r.headers.get("Content-Length", 0)
    )

    current = 0


    with open(filename, "wb") as f:

        for chunk in r.iter_content(
            chunk_size=1024*1024
        ):

            if chunk:

                f.write(chunk)

                current += len(chunk)

                if total:
                    print(
                        f"\r下载进度: {current/total:.2%}",
                        end=""
                    )


    print("\n完成")


download(
    url,
    "test.mp4"
)