# B站视频下载

> 基于 DASH 流的 B站视频爬虫，自动选最高码率，音视频分离下载后 ffmpeg 合并。

## 整体流程

```
BV号
  │
  ▼
① 请求视频页面 HTML
  │  GET https://www.bilibili.com/{bvid}
  ▼
② 正则提取 __INITIAL_STATE__ JSON
  │  获取：bvid / cid / title / wbiImgKey / wbiSubKey
  ▼
③ WBI 签名
  │  imgKey + subKey → MIXIN_KEY_ENC_TAB 重排 → mixin_key
  │  params + wts → 排序 → urlencode → + mixin_key → MD5 → w_rid
  ▼
④ 请求 playurl API（带签名参数）
  │  GET https://api.bilibili.com/x/player/wbi/playurl
  │  params: bvid, cid, qn=112, fnval=4048, fnver=0, fourk=1, wts, w_rid
  ▼
⑤ 解析 DASH 流
  │  分别取 video 和 audio 数组中 bandwidth 最高的条目
  ▼
⑥ 下载 video.m4s + audio.m4s（流式写文件）
  ▼
⑦ ffmpeg 合并 → out/{title}.mp4
  │  ffmpeg -i video.m4s -i audio.m4s -c:v copy -c:a aac output.mp4
  │  合并后删除临时 m4s 文件
```

## 关键参数

| 参数 | 值 | 作用 |
|------|-----|------|
| `qn` | 112 | 请求 1080P+ 画质 |
| `fnval` | 4048 | 位掩码，启用 DASH + 4K + HDR + 杜比全格式 |
| `fourk` | 1 | 允许服务端返回 4K 信息（非保证） |

## 技术点

- **WBI 签名**：B站 API 反爬核心，mixin_key 重排表固定 64 位，截前 32 位参与 MD5
- **DASH 流**：音视频分离为两个 m4s 文件，需分别下载后合并
- **码率选择**：`max(dash["video"], key=lambda x: x["bandwidth"])` 自动取最高
- **安全文件名**：`re.sub(r'[\\/:*?"<>|]', '_', title)` 过滤 Windows 非法字符

## 运行

```bash
python 实战-DASH流视频下载.py
# 输入 BV 号即可
```

## 依赖

- Python: `requests`
- 外部工具: `ffmpeg`（需在 PATH 中）

## 文件

| 文件 | 说明 |
|------|------|
| `实战-DASH流视频下载.py` | 主脚本 |
| `API参数参考.md` | B站 API 参数映射表与签名机制 |
| `out/` | 下载输出目录 |
