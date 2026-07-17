import re

content = 'Hello 1234567 World_This is a Regex Demo'

result = re.match('^He.*(\d+).*Demo$', content)
print(result)
print(result.group(1))
# 7
# .*会尽可能多的匹配字符
# .*后面的\d+, 也就是至少一个数字, 并没有指定具体多少个数字
# 因此.*尽可能多的匹配数字, 给\d+只留满足条件的字符

result = re.match('^He.*?(\d+).*Demo$', content)
print(result)
print(result.group(1))
# 1234567
# 所以在做匹配时, 字符串中间尽量用非贪婪匹配
# 也就是用.*?来代替.*
# 以免出现匹配结果丢失的情况