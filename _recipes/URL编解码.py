"""
原项目 -projects/视频/抖音喜欢视频/
功能   URL百分号编解码（urllib.parse的quote与unquote）
"""

from urllib.parse import unquote

s = "%E5%BE%A1%E5%A7%90%20%E8%B7%B3%E8%88%9E"

print(unquote(s))

from urllib.parse import quote

s = "御姐 跳舞"

print(quote(s))