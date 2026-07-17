from bs4 import BeautifulSoup

# 创建一个BeautifulSoup的工具对象，然后把即将被解析的页面源码数据加载到该对象中
fp = open(r'F:\code_practice\code\python\00-爬虫\爬虫&逆向\Day03数据解析\test.html', 'r', encoding='utf-8')
# 参数1：被解析的页面源码数据
# 参数2：固定形式的lxml(一种解析器)
soup = BeautifulSoup(fp, 'lxml')


# *************************标签定位********************
# 方式1: 标签名定位
# soup.tagName(tagName是标签名，只可以定位到第一次出现的该标签)
# title标签
title_tag = soup.title
print("soup.title:", title_tag) 
# p标签
p_tag = soup.p
print("p.tag:", p_tag)      

# 方式2: 属性定位
# soup.find(tagName,attrName='value')  tagName是标签名,attrName是属性名
# 定位到class属性值为song的div标签
div_tag = soup.find('div', class_='song')
print("div_tag:", div_tag)
# 定位到class属性值为du的a标签
a_tag = soup.find('a', class_='du')
print("a_tag:", a_tag)
# 定位到id的属性值为feng的a标签
a_tag = soup.find('a', id='feng')
print("a_tag:", a_tag)

# 定位所用p标签
p_all_tag = soup.find_all('p')
print("p_all_tag:", p_all_tag)
# 定位所有属性为song的div标签
div_all_tag = soup.find_all('div', class_='song')
print("div_all_tag:", div_all_tag)

# 方式3: 选择器定位 class选择器(.class属性值) id选择器(#id的属性值)
# 定位到id的属性值为feng对应的所有标签,以列表形式输出
tags = soup.select('#feng')  
print("id选择器:", tags)
# 定位到class属性值为du对应的所有标签，以列表的形式输出
tags = soup.select('.du')  
print("class选择器:", tags)

# 方式4: 层级选择器：>表示一个层级 一个空格可以表示多个层级
# tags = soup.select('.tang > ul > li > a')
tags = soup.select('.tang a')
print("层级选择器:", tags)


# *************************数据提取********************
# 方式1：提取标签内的文本数据
tag = soup.select("#feng")[0]  # 因为select获取的标签以列表的形式输出，所以可以通过列表的形式[0]获取
print("文本值提取:", tag.string) # tag.string:只可以将标签直系的文本内容提取出
print("文本值提取:", tag.text)   # tag.text:可以将标签内部所有的文本内容提取出，包括当前标签

# 方式2：提取标签的属性值  tag['attrName']
img_src = soup.find('img')['src']    # 获取该标签的src属性的值
print("图片标签属性值:", img_src)  