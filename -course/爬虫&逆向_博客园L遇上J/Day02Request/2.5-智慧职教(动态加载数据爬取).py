import requests

# 指定url
url = "https://www.icve.com.cn/prod-api/goodCourse/list?page=5"

# 发送请求
response = requests.get(url)

# 获取响应数据
page_text = response.json()

for dict in page_text['rows']:
    courseName = dict['courseName']
    schoolName = dict['schoolName']
    courseUrl  = dict['courseUrl']
    print(courseName, schoolName, courseUrl)