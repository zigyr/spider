import re

text = "username=admin&password=123456"

m = re.search(
    r'username=(\w+)&password=(\w+)',
    text
)

username, password = m.groups()

print(username)
print(password)