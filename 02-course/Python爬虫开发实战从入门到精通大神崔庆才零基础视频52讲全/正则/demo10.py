import re

text = "我的手机号：13812345678"

m = re.search(r'(1)(3\d)(\d{4})(\d{4})', text)

head, operator, middle, tail = m.groups()

print(head)
print(operator)
print(middle)
print(tail)