from lxml import etree

# 创建一个etree的工具对象，然后把即将被解析的页面源码数据加载到该对象中
tree = etree.parse(r"F:\code_practice\code\python\00-爬虫\爬虫&逆向\Day03数据解析\test.html")

# xpath函数返回的是列表，列表中存储的是满足定位要求的所有标签

# *********************************************    标签定位   ****************************************
# /html/head/title
# 定位到html下面的head下面的title标签
title_tag = tree.xpath('/html/head/title')
print("title_tag:", title_tag)

# //title在页面源码中
# 定位所有的符合要求的title标签
title_tags = tree.xpath('//title')
print("title_tags:", title_tag)

# 定位到所有的符合要求的div标签
div_tags = tree.xpath('//div')
print("div_tags:", div_tags)

# 属性定位
# 定位到class属性值为song的div标签 //tagName[@attrName='value']
div_class_song_tag = tree.xpath('//div[@class="song"]')
print("div_class_song_tag:", div_class_song_tag)

# 索引定位: 索引是从1开始的
# 获取第一个div
div_fir_tag = tree.xpath('//div[1]')
print("div_fir_tag:", div_fir_tag)

# 层级定位: /表示一个层级  //表示多个层级
a_list = tree.xpath('//div[@class="tang"]/ul/li/a')
print("a_list:", a_list)
a_list = tree.xpath('//div[@class="tang"]//a')
print("a_list:", a_list)

# *********************************************    数据提取   ****************************************
# 提取数据: /text()提取直系文本 //text()提取所有文本 [都是以列表的形式输出]
a_content = tree.xpath("//a[@id='feng']/text()")
print(a_content)
a_content = tree.xpath("//div[@class='song']//text()")
print(a_content)

# 提取标签的属性值：//tag/@attrName
text_url = tree.xpath("//div[@class='tang']//a/@href")
print(text_url)