# cn.xgroovy.com — HTTP Range 多线程视频下载器

**Date:** 2026-07-16
**Author:** zigyr

## 概述

针对 cn.xgroovy.com 视频站的完整下载管线。通过 XPath 解析视频页面获取真实媒体地址，利用 HTTP Range + ThreadPoolExecutor 实现多线程分片并发下载，再以随机写入完成文件重组。

## 技术链路

```
输入 URL → fetch_page (GET HTML) → parse_page (XPath 提取 video_url + title)
→ download_range (HEAD 取文件大小 → 计算 Range 切片 → 8线程分片下载 → seek+write 随机写入合并)
→ 完整 MP4
```

## 技术栈

| 技术 | 用途 |
|------|------|
| requests + Session | HTTP 请求管理 |
| lxml + XPath | 页面解析、资源定位 |
| HTTP HEAD | 获取 Content-Length |
| HTTP Range | 文件分片传输 |
| ThreadPoolExecutor | 多线程并发下载 |
| seek() + write() | 随机位置写入文件 |
| pyperclip | 剪贴板读取 SessionBuddy URL 列表 |
| re | URL 正则提取 |

## 目录结构

| 文件 | 说明 |
|------|------|
| [实战-HTTP-Range多线程下载.py](实战-HTTP-Range多线程下载.py) | 主程序 |
| [todo.md](todo.md) | 优化清单 |
| `out/video/` | 下载输出目录 |

## 依赖

```bash
pip install requests lxml pyperclip
```

## 使用方式

两种输入模式：

1. **手动模式**：代码内预置 URL 列表，直接运行
2. **剪贴板模式**：从 SessionBuddy 复制 `title & url` 列表，脚本自动从剪贴板正则提取所有 URL

```bash
python 实战-HTTP-Range多线程下载.py
```

按提示输入 `1`（手动）或 `2`（剪贴板读取）。

## 相关经验片段

| 片段 | 路径 |
|------|------|
| 检测服务器是否支持 Range 请求 | [_recipes/检测服务器是否支持Range请求.py](../../_recipes/检测服务器是否支持Range请求.py) |
| 从剪贴板提取 URL | [_recipes/从剪切板提取URL.py](../../_recipes/从剪切板提取URL.py) |
