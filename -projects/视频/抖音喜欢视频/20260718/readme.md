喜欢视频
api-1: https://www.douyin.com/aweme/v1/web/aweme/favorite/
api-2: https://www-hj.douyin.com/aweme/v1/web/aweme/favorite/


headers:
referer: 仅必须含有/search/url编码的搜索内容
cookie
params:
aid



打开抖音，随便在个人页面的喜欢的页面上下滑动

搜索/favorite搜索api入口

复制至自动生成爬虫的网站

然后就是生成json, 解析json, 下载数据




今天是2026-07-22，又重新运行了一下这个脚本

发现了两个非常神奇的事情

第一个，这个程序竟然还能跑

其次，他竟然还能神奇的生成动态的json数据
也就是说，json中的数据，与上次代码生成的不一样，因为我这几天也在刷抖音
所以这个api的接口，其实就是抖音喜欢那一栏视频的请求对象，目前一次性的下载量是19个
我认为这也是params的事情
而
```python
cookies = {
    'sid_guard': '2396842c36309e1898616cfd41f16ecb%7C1783143834%7C5184000%7CWed%2C+02-Sep-2026+05%3A43%3A54+GMT',
    'ttwid': '1%7C8kecg4UAA3FMw_hlCgjMDKEGKgrjopaSW-xam89EiT8%7C1784355005%7C0205c28397847f5c9df09442a93deeb5e37665a323dc3a20a90f7c641ba1955f',
}
params = {
    'aid': '6383',
}
```
对于aid、sid_guard、ttwid的逆向就会很有价值
与时间戳无关
那这个任务就放在后续某个节点进行
今天2026-07-22，先去试试抖音图文视频的下载逻辑