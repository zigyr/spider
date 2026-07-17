import requests
from urllib.parse import urljoin

BASE_URL = 'https://login3.scrape.center'
LOGIN_URL = urljoin(BASE_URL, 'api/login')
INDEX_URL = urljoin(BASE_URL, '/api/book')
USERNAME = 'admin'
PASSWORD = 'admin'

r_login = requests.post(LOGIN_URL, json={'username': USERNAME, 'password': PASSWORD})
data = r_login.json()
print('Response JSON', data)
jwt = data.get('token')
print('JWT', jwt)

headers = {
    'Authorization': f'jwt {jwt}'
}
r_index = requests.get(INDEX_URL, params={'limit':18, 'offset':0}, headers=headers)
print('Response Status', r_index.status_code)
print('Response URL', r_index.url)
print('Response Data', r_index.json())