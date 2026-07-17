import requests
from urllib.parse import urljoin

BASE_URL = 'https://login2.scrape.center'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

r_login = requests.post(LOGIN_URL, data={'username':USERNAME, 'password':PASSWORD}, allow_redirects=False)
cookies = r_login.cookies
print('Cookies', cookies)

r_index = requests.get(INDEX_URL, cookies=cookies)
print('Response Status', r_index.status_code)
print('Response URL', r_index.url)