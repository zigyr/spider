# 抖音喜欢视频 — 批量下载

**Date:** 2026-08-02
**Author:** zigyr

## 概述

通过抖音 Web API 获取喜欢/用户视频列表，实现从接口监听到批量下载的完整自动化链路。项目经历了三个阶段演进：

```
Phase 1 (0718): 手动抓包复制 JSON → requests 同步下载
Phase 2 (0801): DrissionPage 浏览器接管 → 绕过签名 → API 实时拦截
Phase 3 (0802): 全自动链路 → API拦截 → JSON存储 → aiohttp 异步批量下载 + tqdm 进度条
```

## 技术链路（当前推荐）

```
DrissionPage 浏览器接管
        ↓
tab.listen.start() 拦截 aweme/post API
        ↓
解析 aweme_list → 提取 title / url / id
        ↓
逐页监听 → has_more=0 结束
        ↓
aiohttp 异步并发下载 (Semaphore限流 + 指数退避重试)
        ↓
tqdm 进度条可视化
```

## 目录结构

| 路径 | 说明 |
|------|------|
| `20260718/` | Phase 1：requests 同步下载（手动 JSON） |
| `20260719/` | 探索：API 参数分析 |
| `20260722/` | 深度研究：图文下载、timestamp、视频合成 |
| `20260801/` | Phase 2：DrissionPage 浏览器接管 + API 监听 + 阶段复盘 |
| `20260802/` | Phase 3：全自动链路 — 拦截→存储→异步下载→进度条 |
| [note.md](note.md) | 零散发现：单视频页 URL 模式 `?modal_id=video_id` |
| [TODO.md](TODO.md) | 待优化项清单 |

### 20260802 脚本清单

| 文件 | 说明 |
|------|------|
| [实战-DrissionPage接口监听与数据提取.py](20260802/实战-DrissionPage接口监听与数据提取.py) | 浏览器接管 → 拦截 aweme/post → 提取视频信息 → 存 JSON |
| [基础-视频直链下载验证.py](20260802/基础-视频直链下载验证.py) | 验证 CDN 直链无需特殊请求头即可下载 |
| [进阶-aiohttp异步批量下载.py](20260802/进阶-aiohttp异步批量下载.py) | aiohttp 并发下载 + Semaphore 限流 + 指数退避重试 |
| [进阶-tqdm进度条异步下载.py](20260802/进阶-tqdm进度条异步下载.py) | 上者的升级版：tqdm 进度条 + 成功/失败统计 |
| [基础-JSONL逐行写入与读取.py](20260802/基础-JSONL逐行写入与读取.py) | JSONL 格式：逐行追加写入替代一次性 json.dump |

### 已提取到经验库

| 经验片段 | 路径 |
|----------|------|
| URL 编解码 | [_recipes/URL编解码.py](../../_recipes/URL编解码.py) |
| 从 JSON 提取视频 URL | [_recipes/从JSON提取视频URL.py](../../_recipes/从JSON提取视频URL.py) |

## 依赖

```bash
pip install requests          # Phase 1 同步下载
pip install DrissionPage      # Phase 2/3 浏览器接管
pip install aiohttp aiofiles  # Phase 3 异步下载
pip install tqdm              # Phase 3 进度条
```

## 使用步骤（当前推荐方式）

### 1. 拦截 API + 提取数据

```bash
cd 20260802
python 实战-DrissionPage接口监听与数据提取.py
```

- 自动打开 Edge 浏览器（使用已有登录态 `E:\EdgeProfile`）
- 监听 `aweme/post` 接口，逐页收集视频信息
- 每 50 条自动保存，最终写入 `video.json`

### 2. 异步批量下载

```bash
python 进阶-tqdm进度条异步下载.py
```

- 读取 `video.json`，aiohttp 并发下载（最多 10 个同时）
- 失败自动重试 3 次（指数退避 2s → 4s → 8s）
- tqdm 实时进度条 + 成功/失败统计
- 视频输出到 `out/`，文件名格式：`{标题}_{视频ID}.mp4`

## 关键发现

| 发现 | 详情 |
|------|------|
| **签名绕过** | DrissionPage 接管浏览器后，`a_bogus` / `x-secsdk-web-signature` 由浏览器 JS 自动生成，无需手动逆向 |
| **API 端点** | `v1/web/aweme/post/`（用户视频列表），非 favorite API |
| **分页机制** | `max_cursor` 游标分页，`has_more` 判断是否有下一页 |
| **CDN 直链** | 视频 URL 无需 Referer 或其他特殊头，直接 GET 即可 |
| **单视频页** | `https://www.douyin.com/user/{up_id}?modal_id={video_id}` |
| **scroll 无效** | `tab.scroll.to_bottom()` 不触发翻页，抖音非简单滚动加载 |

## 已知限制

- **需手动翻页**：当前分页仍依赖手动滚动浏览器让前端触发下一页请求（DrissionPage 监听被动接收），尚未找到程序化触发分页的 JS 入口
- **仅视频**：图文/图集未处理
