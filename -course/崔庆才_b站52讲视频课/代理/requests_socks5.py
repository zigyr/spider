import requests

proxy = "127.0.0.1:7890"

# pip install "requests[socks]"
proxies = {
    "http": "socks5://" + proxy,
    "https": "socks5://" + proxy
}

try:
    r = requests.get("https://httpbin.org/get", proxies=proxies)
    print(r.text)
except requests.exceptions.ConnectionError as e:
    print('Error:', e.args)