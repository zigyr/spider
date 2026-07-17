import re

content = """Hello 1234567 World_This
is a Regex Demo
"""

result = re.match(r'^Hello.*?(\d+).*Demo$', content, re.S)
print(result)
print(result.group(1))