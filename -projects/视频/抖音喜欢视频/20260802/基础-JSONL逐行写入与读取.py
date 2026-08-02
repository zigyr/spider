import os

worker_folder = os.path.dirname(os.path.abspath(__file__))

for item in data["aweme_list"]:
    video = {
        "title": item["desc"],
        "url": item["video"]["play_addr"]["url_list"][0]
    }
    with open(
        "videos.jsonl",
        "a",  # 直接追加写入, 一行就是一个json对象
        encoding="utf-8"
    ) as f:
        f.write(
            json.dumps(
                video,
                ensure_ascii=False
            )
            + "\n"
        )

import json
video_list = []
with open(
    "videos.jsonl",
    "r",
    encoding="utf-8"
) as f:
    for line in f:
        video = json.loads(line)
        video_list.append(video)
print(video_list)