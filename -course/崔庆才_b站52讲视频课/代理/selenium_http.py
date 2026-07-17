from selenium import webdriver
from selenium.webdriver.chrome.options import Options

proxy = "127.0.0.1:7890"
options = Options()
options.add_argument("--start-maximized")
options.add_argument(f"--proxy-server=http://{proxy}")
driver = webdriver.Chrome(options=options)
driver.get("https://httpbin.org/get")
print(driver.page_source)
driver.quit()