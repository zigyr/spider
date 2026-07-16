# Spider — Python 爬虫学习与实战

基于 Python 的网络爬虫学习项目，涵盖从基础请求到高级逆向工程的全链路实践。仓库内容随学习进度持续更新。

## 项目结构

```
spider/
├── 01-basics/          # 基础入门：HTTP 请求、代理、文件操作
├── 02-course/          # 课程笔记：多来源爬虫教程随堂代码
├── 03-dll/             # 工具库：可复用下载器、并发模块、流媒体处理
├── 04-projects/        # 实战项目：图片 / 文字 / 视频爬取
├── _notes/             # 零散笔记与踩坑记录
└── journal/            # 自动生成的学习日志
```

## 目录说明

### 01-basics — 基础入门

零基础起步，掌握 HTTP 请求与响应、请求头处理、代理配置、页面解析、文件下载等核心基础操作。

### 02-course — 课程笔记

跟随多个爬虫教程的实战代码，覆盖从入门到逆向的完整学习路径：

| 来源 | 涉及主题 |
|------|----------|
| **崔庆才《Python爬虫开发实战》** | 代理、多线程/多进程、模拟登录、验证码识别 |
| **博客园 L遇上J 系列** | Request → 数据解析 → 高级反爬 → 综合实战 → JS 基础/进阶 → JS 逆向核心 |
| **NightTeam 逆向** | JS 逆向专项 |

### 03-dll — 可复用工具库

从简单到生产级的渐进式工具实现：

| 模块 | 内容 |
|------|------|
| `downloader/` | 同步阻塞 → Session 复用 → 线程池并发 → 指数退避重试 → aiohttp 异步，逐级演进 |
| `concurrency/` | 多线程 / 多进程并发复制 |
| `video/` | M3U8 流解析与 AES 解密、MP4 流式下载 |

### 04-projects — 实战项目

针对具体网站的完整爬取方案，按类型组织：

| 类型 | 示例 |
|------|------|
| 🖼️ 图片 | 随机图 API 调用、图片站批量爬取 |
| 📝 文字 | 小说章节下载、博客内容提取 |
| 🎬 视频 | M3U8 视频解密下载、直链流式下载 |

## 技术栈

- **语言**: Python 3
- **网络请求**: `requests`, `aiohttp`, `httpx`
- **并发**: `concurrent.futures`（线程池/进程池）、`asyncio`
- **解析**: `BeautifulSoup`, `lxml`/`xpath`, 正则
- **逆向**: AES-CBC 解密、M3U8 流解析、JS 逆向、Selenium 自动化
- **其他**: `pycryptodome`、`chardet`、`tqdm`

## 快速开始

```bash
pip install requests aiohttp pycryptodome beautifulsoup4 lxml

python 01-basics/1、简单的get请求和响应.py
```

## 注意事项

- 本项目仅供学习交流，请遵守目标网站的 `robots.txt` 与服务条款
- 爬取的图片/视频数据（`**/out/`）已通过 `.gitignore` 排除，不纳入版本控制
- `_notes/` 目录下的笔记文件建议在运行相关脚本前阅读
