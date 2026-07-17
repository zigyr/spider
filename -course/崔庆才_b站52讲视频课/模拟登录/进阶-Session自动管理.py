import requests
from urllib.parse import urljoin

BASE_URL = 'https://login2.scrape.center'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

session = requests.session()

r_login = session.post(LOGIN_URL, data={'username':USERNAME, 'password':PASSWORD})

# r_login.cookies没有结果
# 原因是`allow_redirects=True`的情况下, r_login重定向至r_index,并不保存重定向前r_login的set_cookie字段信息
# 但这部分信息, 会被session保存, 这也就是session.cookies可以的原因
cookies = session.cookies
print('Cookies', cookies)

r_index = session.get(INDEX_URL)
print('Response Status', r_index.status_code)
print('Response URL', r_index.url)