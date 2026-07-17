"""
超级鹰验证码识别 API 封装
官方文档: http://www.chaojiying.com/api.html
"""

import requests
from hashlib import md5
from typing import Dict, Any


class ChaojiyingError(Exception):
    """超级鹰 API 异常"""
    pass


class Chaojiying:
    """超级鹰打码平台客户端"""

    BASE_URL = "http://upload.chaojiying.net/Upload/Processing.php"
    REPORT_URL = "http://upload.chaojiying.net/Upload/ReportError.php"
    TIMEOUT = 30  # 秒

    def __init__(self, username: str, password: str, soft_id: int):
        self.username = username
        self.password = md5(password.encode("utf-8")).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            "user": self.username,
            "pass2": self.password,
            "softid": self.soft_id,
        }
        self.headers = {
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
        }

    def post_pic(self, im: bytes, codetype: int) -> Dict[str, Any]:
        """
        上传图片识别

        Args:
            im: 图片字节数据
            codetype: 验证码类型，参考 http://www.chaojiying.com/price.html
                      9102: 文字点选

        Returns:
            API 返回的 JSON 字典

        Raises:
            ChaojiyingError: 识别失败或网络异常
        """
        params = {"codetype": codetype}
        params.update(self.base_params)
        files = {"userfile": ("captcha.png", im)}

        try:
            resp = requests.post(
                self.BASE_URL,
                data=params,
                files=files,
                headers=self.headers,
                timeout=self.TIMEOUT,
            )
            resp.raise_for_status()
            result = resp.json()
        except requests.RequestException as e:
            raise ChaojiyingError(f"网络请求失败: {e}") from e
        except ValueError as e:
            raise ChaojiyingError(f"API 返回非 JSON 数据: {e}") from e

        err_no = result.get("err_no")
        if err_no is None:
            raise ChaojiyingError(f"API 返回格式异常: {result}")

        if err_no != 0:
            err_str = result.get("err_str", "未知错误")
            raise ChaojiyingError(f"识别失败 [{err_no}]: {err_str}")

        return result

    def report_error(self, im_id: str) -> Dict[str, Any]:
        """
        上报识别错误（返还点数）

        Args:
            im_id: 图片 ID（从 post_pic 返回结果中获取）
        """
        params = {"id": im_id}
        params.update(self.base_params)
        try:
            resp = requests.post(
                self.REPORT_URL,
                data=params,
                headers=self.headers,
                timeout=self.TIMEOUT,
            )
            return resp.json()
        except requests.RequestException as e:
            raise ChaojiyingError(f"报错请求失败: {e}") from e
