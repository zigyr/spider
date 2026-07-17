"""
出现空白字符就写\s匹配, 出现数字就用\d匹配
工作量非常大
可以用.*这个万能匹配来减少这些工作
.匹配任意字符(除换行符)
*匹配前面的字符无限次
还请注意, 在.*中, *所匹配的前面的字符是.
所以其实是(.)*
"""
import re

content = 'Hello 123 4566 World_This is a Regex Demo'

result = re.match(r'^Hello.*Demo$', content)
print(result)
print(result.group())
print(result.span())