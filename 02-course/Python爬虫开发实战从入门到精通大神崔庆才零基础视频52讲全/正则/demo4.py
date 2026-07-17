import re

content = 'Hello 1234567 World_This is a Regex Demo'

# result = re.match(r'^Hello.\d*\s.*Demo$', content)
result = re.match(r'^Hello\s\d+\s\w+\s\w+\s\w+\s\w+\sDemo$', content)
print(result)
print(result.group())
print(result.span()) 