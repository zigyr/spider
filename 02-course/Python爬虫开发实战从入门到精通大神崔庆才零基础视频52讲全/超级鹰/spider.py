"""
极验(Geetest) 文字点选验证码破解 — 目标站: captcha3.scrape.center

原始代码问题:
  1. 截图裁剪未乘以 devicePixelRatio → 高 DPI 屏坐标完全偏移
  2. `button[type="button"]` 选择器过于宽泛
  3. 零异常处理，任一步超时就崩溃
  4. 硬编码 sleep，无显式等待条件
  5. __del__ 用 close() 而非 quit()，残留 Chrome 进程

核心修复:
  - DPI 感知截图: CSS 坐标 × devicePixelRatio = 截图像素坐标
  - 图片获取: JS Canvas 导出优先 → 截图裁剪回退
  - 坐标对齐: img.geetest_item_img 为参照系（非面板 box，面板有标题栏偏移）
  - JS 原生点击: MouseEvent 派发，比 ActionChains.move_to_element_with_offset 更精确
  - 上下文管理器 + 重试 + 浏览器重启规避指纹
"""

from __future__ import annotations

import time
import logging
import argparse
from io import BytesIO
from pathlib import Path
from typing import List, Optional

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from chaojiying import Chaojiying, ChaojiyingError

# ============================================================================
# 配置
# ============================================================================

USERNAME = "admin"
PASSWORD = "admin"

CHAOJIYING_USERNAME = "2026071682et87b0"
CHAOJIYING_PASSWORD = "09v5bssf"
CHAOJIYING_SOFT_ID = 893590
CHAOJIYING_KIND = 9102  # 文字点选，见 http://www.chaojiying.com/price.html

TARGET_URL = "https://captcha3.scrape.center/"
MAX_RETRIES = 3

DEBUG_DIR = Path(__file__).parent / "_debug"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("crack")


# ============================================================================
# 核心类
# ============================================================================


class CrackCaptcha:
    """极验文字点选验证码破解器 — Selenium + 超级鹰"""

    def __init__(self, headless: bool = False, debug: bool = False) -> None:
        self.url = TARGET_URL
        self.headless = headless
        self.debug = debug
        self.browser: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self._dpr: float = 1.0
        self.chaojiying = Chaojiying(
            CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID
        )
        if self.debug:
            DEBUG_DIR.mkdir(exist_ok=True)

    # ---- 上下文管理 ----

    def __enter__(self) -> "CrackCaptcha":
        self.browser = self._create_browser()
        self.wait = WebDriverWait(self.browser, 20)
        self._dpr = self.browser.execute_script("return window.devicePixelRatio")
        logger.info(f"浏览器就绪 | DPR={self._dpr} | headless={self.headless}")
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb) -> None:
        if self.browser:
            self.browser.quit()
            logger.info("浏览器已关闭")

    def _create_browser(self) -> webdriver.Chrome:
        opts = webdriver.ChromeOptions()
        if self.headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        browser = webdriver.Chrome(options=opts)
        browser.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        return browser

    # ---- 页面操作 ----

    def open(self) -> None:
        """打开登录页，填入账号密码，等待极验 JS 初始化"""
        logger.info(f"打开: {self.url}")
        self.browser.get(self.url)

        user = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]'))
        )
        pwd = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
        )
        user.clear()
        user.send_keys(USERNAME)
        pwd.clear()
        pwd.send_keys(PASSWORD)
        logger.info("已填入账号密码")

        # 等待极验 JS 库加载 (避免点击登录时 Geetest 尚未初始化)
        try:
            self.wait.until(
                lambda d: d.execute_script(
                    "return typeof initGeetest !== 'undefined'"
                )
            )
            logger.info("极验 JS 库已就绪")
        except TimeoutException:
            logger.warning("极验 JS 未检测到")

    def click_login(self) -> None:
        """点击登录按钮触发验证码"""
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-button--primary"))
        ).click()
        logger.info("已点击登录按钮")

    def wait_for_panel(self) -> None:
        """等待极验面板出现 + 验证码图片加载完毕"""
        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "geetest_panel_box"))
        )
        logger.info("验证码面板已出现")

        # 等待面板从 loading 态切换为可操作态
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".geetest_panelshowclick")
                )
            )
            logger.info("面板可操作 (panelshowclick)")
        except TimeoutException:
            logger.warning("面板未进入 click 态")

        # 等待图片加载
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "img.geetest_item_img")
            )
        )
        logger.info("验证码图片已加载")

    # ---- 验证码图片获取 ----

    def _captcha_from_canvas(self) -> Optional[Image.Image]:
        """策略 A: JS 将图片绘制到 canvas 导出 data URI，零坐标偏移"""
        try:
            data_url = self.browser.execute_script("""
                var img = document.querySelector('img.geetest_item_img');
                if (!img) return null;
                var c = document.createElement('canvas');
                c.width = img.naturalWidth || img.width;
                c.height = img.naturalHeight || img.height;
                c.getContext('2d').drawImage(img, 0, 0);
                return c.toDataURL('image/png');
            """)
            if data_url and data_url.startswith("data:image"):
                import base64
                _, b64 = data_url.split(",", 1)
                img = Image.open(BytesIO(base64.b64decode(b64)))
                logger.info(f"[Canvas] 验证码图片: {img.size}")
                return img
        except Exception as e:
            logger.debug(f"[Canvas] 失败: {e}")
        return None

    def _captcha_from_screenshot(self) -> Image.Image:
        """策略 B: 截图裁剪到 img.geetest_item_img 元素 (DPI 修正)"""
        el = self.browser.find_element(By.CSS_SELECTOR, "img.geetest_item_img")
        time.sleep(0.3)

        loc = el.location
        size = el.size
        dpr = self._dpr

        left = int(loc["x"] * dpr)
        top = int(loc["y"] * dpr)
        right = int((loc["x"] + size["width"]) * dpr)
        bottom = int((loc["y"] + size["height"]) * dpr)

        png = self.browser.get_screenshot_as_png()
        full = Image.open(BytesIO(png))
        captcha = full.crop((left, top, right, bottom))

        if self.debug:
            full.save(DEBUG_DIR / "full_screenshot.png")
            captcha.save(DEBUG_DIR / "captcha_crop.png")

        logger.info(f"[截图] {captcha.size}  (CSS: {size['width']}×{size['height']})")
        return captcha

    def get_captcha_image(self) -> Image.Image:
        """获取验证码图片并缩放到 CSS 尺寸（确保与点击坐标系一致）"""
        img = self._captcha_from_canvas()

        if img is None:
            logger.info("Canvas 提取失败，回退截图裁剪")
            img = self._captcha_from_screenshot()

        # 关键：缩放到 CSS 尺寸，使超级鹰返回的坐标与 move_to_element_with_offset 对齐
        el = self.browser.find_element(By.CSS_SELECTOR, "img.geetest_item_img")
        css_w, css_h = el.size["width"], el.size["height"]
        if (img.width, img.height) != (css_w, css_h):
            logger.info(f"缩放: {img.size} → ({css_w}, {css_h})")
            img = img.resize((css_w, css_h))

        if self.debug:
            img.save(DEBUG_DIR / "captcha_final.png")

        return img

    # ---- 识别与交互 ----

    @staticmethod
    def parse_points(result: dict) -> List[List[int]]:
        """解析超级鹰坐标: 'x1,y1|x2,y2' → [[x1,y1],[x2,y2]]"""
        pic_str = result.get("pic_str", "")
        if not pic_str:
            raise ValueError(f"超级鹰未返回坐标: {result}")
        return [[int(n) for n in g.split(",")] for g in pic_str.split("|")]

    def click_words(self, points: List[List[int]]) -> None:
        """
        按坐标依次点击验证码图片。
        使用 JS 派发原生 MouseEvent（比 Selenium ActionChains 坐标更精确）。
        """
        for i, (x, y) in enumerate(points):
            logger.info(f"点击 [{i+1}/{len(points)}]: ({x}, {y})")
            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "img.geetest_item_img"))
            )
            self.browser.execute_script("""
                var img = document.querySelector('img.geetest_item_img');
                if (!img) return;
                var r = img.getBoundingClientRect();
                var o = {clientX: r.left+arguments[0], clientY: r.top+arguments[1],
                         view: window, bubbles: true, cancelable: true};
                ['mousedown','mouseup','click'].forEach(function(t) {
                    img.dispatchEvent(new MouseEvent(t, o));
                });
            """, x, y)
            time.sleep(0.8)

    def click_verify(self) -> None:
        """点击极验提交按钮"""
        self.wait.until(
            lambda d: d.execute_script(
                "var b=document.querySelector('.geetest_commit');"
                "return b && !b.className.includes('geetest_disable')"
            )
        )
        logger.info("极验提交按钮已启用")
        time.sleep(0.3)

        # 优先 Selenium ActionChains（真实鼠标移动），回退 JS 事件
        try:
            btn = self.browser.find_element(
                By.CSS_SELECTOR, ".geetest_commit:not(.geetest_disable)"
            )
            ActionChains(self.browser).move_to_element(btn).click().perform()
            logger.info("已点击提交 (ActionChains)")
        except Exception:
            self.browser.execute_script("""
                var b = document.querySelector('.geetest_commit');
                if (!b) return;
                var r = b.getBoundingClientRect();
                var o = {clientX: r.left+r.width/2, clientY: r.top+r.height/2,
                         view: window, bubbles: true, cancelable: true};
                ['mousedown','mouseup','click'].forEach(function(t) {
                    b.dispatchEvent(new MouseEvent(t, o));
                });
            """)
            logger.info("已点击提交 (MouseEvent)")

    def is_success(self) -> bool:
        """检查是否登录成功"""
        try:
            self.wait.until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "h2"), "登录成功")
            )
            return True
        except TimeoutException:
            return False

    # ---- 主流程 ----

    def crack(self) -> bool:
        """单次破解"""
        self.open()
        time.sleep(2)

        self.click_login()
        time.sleep(2)
        self.wait_for_panel()

        image = self.get_captcha_image()
        buf = BytesIO()
        image.save(buf, format="PNG")

        result = self.chaojiying.post_pic(buf.getvalue(), CHAOJIYING_KIND)
        logger.info(f"超级鹰: pic_id={result.get('pic_id')}, pic_str={result.get('pic_str')}")

        points = self.parse_points(result)
        self.click_words(points)
        self.click_verify()

        # 等待极验回调自动提交表单
        time.sleep(2)
        return self.is_success()

    def crack_with_retry(self, max_retries: int = MAX_RETRIES) -> bool:
        """带重试的破解（每次重试重启浏览器规避指纹检测）"""
        for attempt in range(1, max_retries + 1):
            logger.info(f"{'='*40} 第 {attempt}/{max_retries} 次 {'='*40}")
            try:
                if self.crack():
                    logger.info("✓ 登录成功!")
                    return True
                logger.warning("✗ 验证未通过")
            except (TimeoutException, NoSuchElementException, ChaojiyingError, RuntimeError) as e:
                logger.error(f"异常: {type(e).__name__}: {e}")

            if attempt < max_retries:
                cooldown = 3 + attempt * 2
                logger.info(f"重启浏览器 (冷却 {cooldown}s)...")
                self.browser.quit()
                time.sleep(cooldown)
                self.browser = self._create_browser()
                self.wait = WebDriverWait(self.browser, 20)
                self._dpr = self.browser.execute_script("return window.devicePixelRatio")

        logger.error(f"已重试 {max_retries} 次，全部失败")
        return False


# ============================================================================
# 入口
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="极验验证码破解")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    parser.add_argument("--debug", action="store_true", help="保存调试截图到 _debug/")
    parser.add_argument(
        "-n", "--attempts", type=int, default=MAX_RETRIES,
        help=f"最大重试次数 (默认: {MAX_RETRIES})",
    )
    args = parser.parse_args()

    with CrackCaptcha(headless=args.headless, debug=args.debug) as cracker:
        ok = cracker.crack_with_retry(max_retries=args.attempts)

    raise SystemExit(0 if ok else 1)
