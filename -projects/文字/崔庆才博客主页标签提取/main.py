url = "https://cuiqingcai.com/tags/Selenium/"

import requests
from lxml import etree

r = requests.get(url)

tree = etree.HTML(r.text)

content = tree.xpath('//div[@class="content"]/a/text()')

print(content)

"""
['2022', '2048', 'ACE Data', 'ADSL', 'AI', 'AI编程', 'API', 'AceData Cloud', 'Ajax', 'Audios', 'Bootstrap', 'Bug', 'CDN', 'CQC', 'CSS', 'CSS 反爬虫', 'CV', 'ChatGPT', 'Cookie', 'Django', 'Eclipse', 'Elasticsearch', 'FTP', 'Flux', 'Gemini', 'Git', 'GitHub', 'Google SERP', 'HTML5', 'HTTP', 'Hailuo', 'Hexo', 'Hook', 'IP', 'IT', 'Images', 'JSON', 'JSP', 'JavaScript', 'K8s', 'LOGO', 'Linux', 'MIUI', 'Markdown', 'Midjourney', 'MongoDB', 'MySQL', 'Mysql', 'NBA', 'Nano Banana', 'Nexior', 'OCR', 'OpenCV', 'PHP', 'PPT', 'PS', 'Pathlib', 'PhantomJS', 'Playwright', 'Producer', 'Python', 'Python 爬虫', 'Python3', 'Python3爬虫教程', 'Pythonic', 'Python爬虫', 'Python爬虫书', 'Python爬虫教程', 'QQ', 'RabbitMQ', 'ReCAPTCHA', 'Redis', 'Riffusion', 'SAE', 'SSH', 'SVG', 'Scrapy-redis', 'Scrapy分布式', 'SeeDance', 'SeeDream', 'Selenium', 'Session', 'Shell', 'Sora2', 'Suno', 'TKE', 'TXT', 'Terminal', 'Ubuntu', 'VS Code', 'Veo', 'Vercel', 'Videos', 'Vs Code', 'Vue', 'Web', 'Webpack', 'Web网页', 'Windows', 'Winpcap']
"""