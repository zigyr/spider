video_url = "https://v27-daily-a.douyinvod.com/c05badc33307617670dd47d3275e3a5c/6a60cbcd/video/tos/cn/tos-cn-ve-15c000-ce/oYBeI2Q7BB5ryiGIJkgLih1JQevfU5IDxN3LGA/?a=1128&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&cv=1&br=612&bt=612&cs=0&ds=3&ft=QE6gGqI1ffPdp8~Sa13NvAq-antLjrKyOhauRka22u9WejVhWL6&mime_type=video_mp4&qs=0&rc=OzQ6ZmQ8NGg2NjhoOjk4N0Bpamt4ZWw5cnlvPDMzbGkzNUBgNDA2LmMvXl4xYy82LWAxYSNhNTByMmQ0cS5hLS1kLTVzcw%3D%3D&btag=80000e00088000&cquery=100y_10sH&dy_q=1784724920&feature_id=f5241e7604dff1d9d6c943fd20bd51a2&l=202607222055205534FA1BEBEE1EC6101A"


audio_url = "https://sf11-cdn-tos.douyinstatic.com/obj/ies-music/7285704807086590757.mp3"

import os
import requests


root_dir = os.path.dirname(os.path.abspath(__file__))
outp_dir = os.path.join(root_dir, "out")

os.makedirs(outp_dir, exist_ok=True)


with open(os.path.join(outp_dir, "1.mp4"), "wb") as f:
    r = requests.get(video_url)
    f.write(r.content)


with open(os.path.join(outp_dir, "1.mp3"), "wb") as f:
    r = requests.get(audio_url)
    f.write(r.content)

import subprocess


video_path = os.path.join(outp_dir, "1.mp4")
audio_path = os.path.join(outp_dir, "1.mp3")
output_path = os.path.join(outp_dir, "final.mp4")

cmd = [
    "ffmpeg",
    "-y",
    "-stream_loop",
    "-1",
    "-i",
    video_path,
    "-i",
    audio_path,
    "-t",
    "36",
    "-map",
    "0:v",
    "-map",
    "1:a",
    "-c:v",
    "libx264",
    "-c:a",
    "aac",
    output_path
]
subprocess.run(cmd)