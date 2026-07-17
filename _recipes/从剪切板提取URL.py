"""
原项目 -projects/视频/cn.xgroovy.com/
功能   从剪切板读取数据，避免 input 输入时的 PowerShell 混乱，同时提取 title+url
"""

import re
import pyperclip


text = pyperclip.paste()

urls = re.findall(r'https?://\S+', text)


for i in urls:
    print(i)

"""
ProbiusOfficial/PHPSerialize-labs: 【Hello-CTF labs】PHPSerialize-labs是一个使用php语言编写的，用于学习CTF中PHP反序列化的入门靶场。旨在帮助大家对PHP的序列化和反序列化有一个全面的了解。
https://github.com/ProbiusOfficial/PHPSerialize-labs

0x023 phar 反序列化例题讲解_哔哩哔哩_bilibili
https://www.bilibili.com/video/BV1R24y1r71C?vd_source=15e43889ceb0570c656644d55b87d9fe&p=24&spm_id_from=333.788.videopod.episodes

CTFshow-web入门-反序列化_哔哩哔哩_bilibili
https://www.bilibili.com/video/BV1D64y1m78f/?vd_source=15e43889ceb0570c656644d55b87d9fe

PHP: 序言 - Manual
https://www.php.net/manual/zh/
"""