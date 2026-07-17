"""核心思想
Chrome 原生不支持 带用户名密码的代理（例如 http://user:pass@ip:port
）
于是动态生成一个 Chrome 扩展
扩展里用 chrome.proxy.settings.set() 设置代理
再用 chrome.webRequest.onAuthRequired 自动填写用户名密码
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ip = '127.0.0.1'
port = 7890
username = 'foo'
password = 'bar'

manifest_json = """{
    "name":"Chrome Proxy",
    "version":"1.0.0",
    "manifest_version": 2,

    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    }
}
"""
background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%(ip)s",
            port: %(port)s
          }
        }
      }
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {username: "%(username)s",
            password: "%(password)s"
        }
    }
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
)
""" % {'ip': ip, 'port': port, 'username': username, 'password': password}

import tempfile
tmp = tempfile.NamedTemporaryFile(
    suffix=".zip",
    delete=False
)
plugin_file = tmp.name
tmp.close()
import zipfile
with zipfile.ZipFile(plugin_file, "w") as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)

options = Options()
# 启动 Chrome 后, 点击右上角最大化
options.add_argument("--start-maximized")
options.add_extension(plugin_file)
driver = webdriver.Chrome(options=options)
driver.get('https://httpbin.org/get')
print(driver.page_source)
"""
close()
关闭当前标签页
quit()
关闭整个浏览器
"""
driver.quit()