# B站视频API 参数映射表

## qn — 画质编号

quality number，即画质编号。

| qn | 画质 |
|----|------|
| 16 | 360P |
| 32 | 480P |
| 64 | 720P |
| 80 | 1080P |
| 112 | 1080P+ |
| 116 | 1080P60 |
| 120 | 4K |
| 125 | HDR |
| 126 | 杜比 |
| 127 | 8K |

---

## fnval — 视频流格式

控制返回的视频流格式，值为**位掩码**（可叠加）。

| fnval | 含义 |
|-------|------|
| 0 | 默认 MP4（单文件，无 DASH） |
| 16 | DASH（音视频分离的 m4s 流） |
| 64 | DASH + HDR 支持 |
| 128 | DASH + 4K 支持 |
| 256 | DASH + 杜比视界 |
| 512 | DASH + 杜比全景声 |
| 1024 | DASH + Hi-Res 无损 |
| 2048 | DASH + 8K 支持 |

**常用值**：
- `fnval=4048` = 16+64+128+256+512+1024+2048，请求所有可用格式
- `fnval=16` 仅 DASH 基础流

---

## fnver — 播放协议版本

fnver=0，固定值，基本不用管。

---

## fourk — 4K 开关

fourk=1，表示**允许**服务器返回 4K 信息。

不是"一定返回 4K"，服务器还会判断：
- 账号是否为大会员
- 设备是否支持
- 该视频是否上传了 4K 源

---

## bvid / cid

| 参数 | 全称 | 说明 |
|------|------|------|
| `bvid` | Business Video ID | BV 号，视频的唯一标识（如 `BV14iKU6eEBC`） |
| `cid` | Content ID | 视频分 P 的内容 ID，一个 BV 号下可能有多个 cid（多 P） |

来源：从页面嵌入的 `__INITIAL_STATE__` JSON 中提取：
```
data["videoData"]["bvid"]
data["videoData"]["cid"]
```

---

## WBI 签名机制

B站 API 的反爬签名，流程：

```
img_key + sub_key
       │
       ▼
  MIXIN_KEY_ENC_TAB 重排
       │
       ▼
  截取前 32 位 → mixin_key
       │
params + wts（当前时间戳）
       │
       ▼
  按 key 排序 + urlencode
       │
       ▼
  query 字符串 + mixin_key
       │
       ▼
       MD5 → w_rid
```

最终请求参数包含：`params + wts + w_rid`

两个 key（`wbiImgKey`、`wbiSubKey`）从 `__INITIAL_STATE__` 的 `defaultWbiKey` 中获取。

---

## __INITIAL_STATE__

B站视频页面 HTML 中嵌入的 JSON 数据块，包含视频元信息、WBI 密钥等。

正则提取：
```python
re.search(r'__INITIAL_STATE__\s*=\s*(\{.*?\});', html, re.S)
```

---

## 最小参数集调试法

1. 找到 API 接口 URL
2. 逐个删减参数
3. 用最小参数集验证接口是否正常返回
4. 对最小参数集的内容进行 JS 逆向分析
