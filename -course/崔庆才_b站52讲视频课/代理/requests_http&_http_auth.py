import requests


# 如果代理需要认证
# 同样在代理的前面加上用户名密码即可
# proxy = "username:password@127.0.0.1:7890"
prxoy = "127.0.0.1:7890"

proxies = {
    'http': 'http://' + prxoy,
    'https': 'http://' + prxoy
}

try:
    r = requests.get('https://httpbin.org/get', proxies=proxies)
    print(r.text)
except requests.exceptions.ConnectionError as e:
    print('Error: ', e.args)