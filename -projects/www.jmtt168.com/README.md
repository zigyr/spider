# www.jmtt168.com — 多线程图库爬虫

**Date:** 2026-08-05
**Author:** zigyr

## 概述

爬取 www.jmtt168.com 图库图片。三队列生产者-消费者模式：列表页 → 详情页 → 阅读页 → 图片下载。多线程并发下载，按相册标题自动分文件夹存储。

## 技术链路

```
列表页 (分页遍历)
  ↓ xpath 提取详情链接
详情页
  ↓ xpath 提取阅读页链接
阅读页
  ↓ regex 从 <title> 提取标题 / xpath 提取图片链接
图片下载 (10线程 Session 复用)
```

## 目录结构

| 文件 | 说明 |
|------|------|
| `实战-多线程图库爬虫.py` | 主爬虫：三队列 + 多线程下载 |
| `out/` | 下载输出，按标题分文件夹 |

## 依赖

```bash
pip install requests lxml
```

## 使用方式

```bash
python 实战-多线程图库爬虫.py
```

修改 `product_detail()` 中 `range(1, 2)` 控制分页范围。图片输出到 `out/<相册标题>/`。

## 相关经验片段

| 片段 | 说明 |
|------|------|
| `_recipes/从URL中提取文件名.py` | urlparse + os.path.basename 提取文件名 |
