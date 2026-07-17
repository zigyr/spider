from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

BASE_URL = 'https://login2.scrape.center'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

driver = webdriver.Chrome()
driver.get(BASE_URL)
driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(USERNAME)
driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(PASSWORD)
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
time.sleep(10)

# get cookies from selenium
cookies = driver.get_cookies()
print('Cookies', cookies)
driver.quit()

# set cookies to requests
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

r_index = session.get(BASE_URL)
print('Response Status', r_index.status_code)
print('Response URL', r_index.url)