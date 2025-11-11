from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def manual_verification_login():
    driver = webdriver.Edge()

    try:
        # 访问登录页面
        driver.get("https://example.com/login")

        # 输入手机号
        phone_input = driver.find_element(By.NAME, "phone")
        phone_input.send_keys("你的手机号")

        # 点击发送验证码
        send_btn = driver.find_element(By.ID, "send-code")
        send_btn.click()

        print("验证码已发送，请在60秒内输入...")

        # 等待用户手动输入验证码
        time.sleep(60)

        # 点击登录按钮
        login_btn = driver.find_element(By.ID, "login-btn")
        login_btn.click()

        # 等待登录完成
        time.sleep(5)

        # 保存cookies供后续使用
        cookies = driver.get_cookies()
        return cookies

    except Exception as e:
        print(f"登录失败: {e}")
    finally:
        driver.quit()