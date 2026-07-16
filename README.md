# Spider — Python 爬虫学习与实战

基于 Python 的网络爬虫学习项目，涵盖从基础请求到高级逆向工程的全链路实践。

## 项目结构

```
spider/
├── 01-basics/          # 基础入门：HTTP 请求与响应
├── 02-course/          # 课程笔记：多来源爬虫教程实战
├── 03-dll/             # 工具库：可复用的下载器与并发模块
├── 04-projects/        # 实战项目：图片 / 文字 / 视频 / 综合
└── _notes/             # 使用笔记与踩坑记录
```

## 目录说明

### 01-basics — 基础入门

Python `requests` 库的基础操作练习：

- GET / POST 请求与响应处理
- 请求头（headers）的查看、设置与格式化
- URL 参数上传、代理（proxy）配置
- HTML 页面解析（猫眼电影示例）
- 图片 / PNG 文件的本地下载
- 文件路径拼接等工具操作

### 02-course — 课程笔记

多个爬虫教程的随堂代码与练习：

| 来源 | 内容 |
|------|------|
| **崔庆才《Python爬虫开发实战》** | 代理、多线程、多进程、模拟登录、验证码识别（超级鹰） |
| **博客园 L遇上J 系列** | Day02~Day14：Request → 数据解析 → 高级反爬 → 综合实战 → JS 基础 / 进阶 → JS 逆向核心（响应入口定位、解密、请求加密） |
| **崔庆才个人站点** | Selenium 自动化实战 |

### 03-dll — 可复用工具库

渐进式下载器实现，从简单到生产级：

| 模块 | 文件 | 说明 |
|------|------|------|
| `downloader/` | `1-同步阻塞下载器` | 最基础的 requests 流式下载 |
| | `2-Session复用下载器` | Session 复用，减少连接开销 |
| | `3-ThreadPoolExecutor并发下载器` | 多线程并发下载 |
| | `4_1-稳定型下载器_手写retry_backoff` | 指数退避重试 + 断点续传 |
| | `4_2-稳定型下载器_全局共享session` | 全局 Session 池 + 重试 |
| | `5-aiohttp异步下载器` | 基于 asyncio 的高性能异步下载 |
| `concurrency/` | `多线程视频copy器` | 多线程文件复制 |
| | `多进程视频copy器` | 多进程文件复制 |
| `video/` | `m3u8/` | M3U8 流媒体解析、AES-CBC 解密、TS 切片合并 |
| | `mp4/` | MP4 直链流式下载（带进度条） |

### 04-projects — 实战项目

| 类型 | 项目 | 描述 |
|------|------|------|
| 🖼️ 图片 | `www.dmoe.cc` | 随机图片 API 调用与批量下载 |
| 📝 文字 | `bixuejian.5000yan.com` | 小说章节爬取 |
| | `崔庆才博客主页标签提取` | 博客标签解析 |
| 🎬 视频 | `age-anime-v1` | AGE 动漫站 — M3U8 获取、ACE-128 解密、分集下载 |
| 🔀 综合 | （待扩展） | — |

## 技术栈

- **语言**: Python 3
- **核心库**: `requests`, `aiohttp`, `pycryptodome`
- **并发**: `concurrent.futures` (线程池 / 进程池), `asyncio`
- **逆向**: AES-CBC 解密, M3U8 流解析, JS 逆向基础

## 快速开始

```bash
# 安装依赖
pip install requests aiohttp pycryptodome

# 运行基础示例
python 01-basics/1、简单的get请求和响应.py

# 运行 M3U8 视频下载器
python 03-dll/video/m3u8/main.py
```

## 注意事项

- 本项目仅供学习交流，请遵守目标网站的 `robots.txt` 与服务条款
- 部分实战项目（`04-projects/视频/cn.xgroovy.com`、`04-projects/图片/www.ibbs.pro`）未包含在本仓库中
- `_notes/` 目录下的笔记文件请在运行前阅读
