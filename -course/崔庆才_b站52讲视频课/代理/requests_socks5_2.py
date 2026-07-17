import requests
import socks
import socket

# 已过时
socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7890)
socket.socket = socks.socksocket

try:
    r = requests.get('https://httpbin.org/get')
    print(r.text)
except requests.exceptions.ConnectionError as e:
    print('Error:', e.args)