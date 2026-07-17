import requests
from urllib.parse import urljoin

BASE_URL = 'https://login2.scrape.center'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

# requests直接调用post、get等方法
# 每次请求都是一个独立的请求
r_login = requests.post(LOGIN_URL, data={'username':USERNAME, 'password':PASSWORD})
r_index = requests.get(INDEX_URL)

print('Response Status', r_index.status_code)
print('Response URL', r_index.url)