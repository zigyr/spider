import re

content = 'Hello 123 4566 World_This is a Regex Demo'
print(len(content))

# r raw string
# python不再处理反斜杠
result = re.match(r'^Hello\s\d\d\d\s\d{4}\s\w{10}', content)
print(result)
print(result.group())
# .span 匹配结果在原字符串中的起始位置和结束位置（左闭右开）
print(result.span())
start, end = result.span()
print(start, end, f'"{content[start:end]}"')