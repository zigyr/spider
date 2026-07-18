# 抖音喜欢视频 — 批量下载

**Date:** 2026-07-18
**Author:** zigyr

## 概述

通过抖音 Web API 的喜欢列表接口（`/aweme/v1/web/aweme/favorite/`），批量下载自己点赞过的视频。

## 技术链路

```
浏览器抓包 → 捕获 favorite API → 保存 JSON 响应 → 解析 aweme_list → 提取视频 URL → requests 下载
```

## 目录结构

| 文件 | 说明 |
|------|------|
| [基础-API接口探测.py](基础-API接口探测.py) | 验证 cookie 有效性，测试 favorite API 是否正常返回数据 |
| [实战-批量下载喜欢视频.py](实战-批量下载喜欢视频.py) | 主下载器：读取 JSON → 解析 aweme_list → 批量下载到 `out/` |
| [1.md](1.md) | 开发笔记：API 入口、headers/params 要求、操作流程 |
| `out/` | 下载的视频输出目录（mp4） |
| `超长json数据解析/` | 早期探索时的原始 JSON 数据文件 |

### 已提取到经验库

| 经验片段 | 路径 |
|----------|------|
| URL 编解码 | [_recipes/URL编解码.py](../../_recipes/URL编解码.py) |
| 从 JSON 提取视频 URL | [_recipes/从JSON提取视频URL.py](../../_recipes/从JSON提取视频URL.py) |

## 依赖

- Python 3.8+
- requests

```bash
pip install requests
```

## 使用步骤

1. 浏览器打开 [抖音个人页](https://www.douyin.com/user/self) → 喜欢标签 → F12 开发者工具
2. 下滑加载更多 → Network 面板筛选 `/aweme/v1/web/aweme/favorite/`
3. 复制响应 JSON，保存到本目录下命名为 `3.json`
4. 运行下载脚本：

```bash
python 实战-批量下载喜欢视频.py
```

5. 视频下载到 `out/` 目录，以数字序号命名

## 关键 API 参数

| 参数 | 说明 |
|------|------|
| `aid=6383` | 应用标识，Web 端固定值 |
| `cookie` | 登录态，从浏览器复制 |
| `referer` | 必须包含 `/search/` + URL 编码的搜索关键词 |
