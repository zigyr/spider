# 抖音用户喜欢视频采集项目阶段总结（2026-08-01）

## 一、项目目标

目标：

> 使用 DrissionPage 结合浏览器环境，实现抖音用户视频列表采集。

期望流程：

```
打开抖音用户主页
        ↓
获取视频列表接口
        ↓
自动翻页
        ↓
提取 aweme 数据
        ↓
保存视频信息
```

---

# 二、今天已经完成的部分

## 1. 确认了接口来源

已经通过：

```python
tab.listen.wait()
```

监听到了抖音真实接口请求。

获取方式：

```python
packet.response.body
```

成功拿到了 JSON 响应。

说明：

* 浏览器已经完成登录状态
* Cookie 有效
* JS 已执行
* 签名验证通过

目前不需要自己生成：

```
a_bogus
x-secsdk-web-signature
```

---

# 三、已经分析清楚的数据结构

## Response（响应）

确认核心数据：

```json
{
    "aweme_list": [],
    "max_cursor": xxx,
    "has_more": 1
}
```

其中：

### 视频数据

位置：

```python
data["aweme_list"]
```

例如：

```python
video = {
    "title": item["desc"],
    "url": item["video"]["play_addr"]["url_list"][0],
    "id": item["aweme_id"]
}
```

已经可以正常提取。

---

## 分页字段确认

核心字段：

```python
data["max_cursor"]
```

作用：

下一次请求的分页游标。

流程：

第一次：

```
request:

max_cursor=0
```

响应：

```
max_cursor=1783828862000
```

第二次：

```
request:

max_cursor=1783828862000
```

响应：

```
max_cursor=1781534066000
```

已经确认：

```
response.max_cursor
        ↓
下一次 request.max_cursor
```

---

# 四、已经分析 Payload 请求参数

已经成功获取 Query Parameters：

例如：

```python
{
'device_platform':'webapp',
'aid':'6383',
'sec_user_id':'xxx',
'max_cursor':'0',
'count':'18',
...
}
```

---

## 参数分类

### 业务参数

真正影响数据：

| 参数          | 作用   |
| ----------- | ---- |
| sec_user_id | 目标用户 |
| max_cursor  | 分页   |
| count       | 数量   |

---

### 浏览器环境参数

例如：

```
browser_name
browser_version
screen_width
cpu_core_num
device_memory
```

作用：

风控环境识别。

---

### 签名参数

确认：

```
a_bogus
x-secsdk-web-signature
msToken
verifyFp
fp
```

属于动态生成。

---

# 五、已经确认失败的方案

## 方案1：requests直接复现接口 ❌

尝试思路：

```
requests
+
拼接max_cursor
+
发送请求
```

失败原因：

修改：

```
max_cursor
```

但是：

```
a_bogus
x-secsdk-web-signature
```

没有重新生成。

服务器验证：

```
参数
+
签名
```

不一致。

结果：

```
403
```

---

## 方案2：DrissionPage简单滚动翻页 ❌

尝试：

```python
tab.scroll.to_bottom()
```

以及：

```python
tab.scroll.down(800)
```

没有触发新的接口请求。

说明：

抖音不是简单：

```
页面滚动
    ↓
请求下一页
```

而是：

```
前端组件状态
    ↓
触发加载逻辑
    ↓
请求接口
```

---

# 六、目前项目卡点

现在已经不是：

❌ 找不到接口

❌ 不知道参数

❌ 不知道分页方式

这些已经解决。

当前卡点：

## 如何触发下一页请求

也就是：

第一次：

```
max_cursor=0
        ↓
成功
        ↓
得到max_cursor
```

但是：

如何让浏览器发送：

```
max_cursor=1783828862000
```

目前未知。

---

# 七、下一阶段可能方向

## 方向1（推荐）

研究抖音前端加载逻辑：

目标：

找到：

```
加载更多函数
```

例如：

```
loadMore()
getPostList()
fetchAweme()
```

然后：

通过：

```python
tab.run_js()
```

调用。

让：

```
网页JS
 ↓
生成签名
 ↓
发送请求
```

---

## 方向2

继续研究 DOM：

寻找：

* 视频列表容器
* 内部滚动区域
* 加载更多触发元素

因为：

```
window滚动
```

可能不是目标元素。

---

## 方向3（难度最高）

完整逆向：

分析：

```
a_bogus
x-secsdk-web-signature
```

然后：

```
aiohttp/requests
+
自己生成签名
```

完全脱离浏览器。

---

# 八、当前项目状态总结一句话

> 已经完成抖音接口定位、Response 数据解析、Payload 参数分析以及 max_cursor 分页机制确认；已经证明 requests 方案因无法生成动态签名不可行，也证明简单滚动无法触发分页。目前剩余问题是如何让浏览器端 JS 主动触发下一页请求，或者寻找前端分页调用入口。

---

# 九、下次继续时的切入点

建议直接从这里开始：

```
DrissionPage监听到第一次请求
        ↓
获取 aweme/post 接口
        ↓
研究 Network → Initiator
        ↓
寻找是谁调用这个接口
        ↓
定位分页函数
        ↓
浏览器执行该函数
```

不要再从：

```
requests
max_cursor拼接
```

开始，因为这条路已经验证失败。你现在距离成功差的是“触发分页”，不是接口获取。
