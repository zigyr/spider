import requests

proxies = {
    'http': 'http://127.0.0.1:1420',
    'https': 'http://127.0.0.1:1420'
}
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}
url='https://www.youtube.com/'
response=requests.get(url,proxies=proxies,headers=headers)
print(response.status_code)