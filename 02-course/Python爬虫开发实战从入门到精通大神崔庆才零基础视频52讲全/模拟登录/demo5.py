import requests
from urllib.parse import urljoin

BASE_URL = 'https://login3.scrape.center'
LOGIN_URL = urljoin(BASE_URL, '/login')

r_login = requests.post(
    LOGIN_URL,
    json={
        'username': 'admin',
        'password': 'admin'
    }
)

print("status:", r_login.status_code)
print("url:", r_login.url)
print("content-type:", r_login.headers.get("Content-Type"))
print("text:")
print(r_login.text)