from selenium import webdriver

def setup_driver_alternative():
    """
    尝试使用其他浏览器作为备选
    返回: 可用的浏览器驱动实例
    """
    # 尝试 Edge（Windows 系统通常自带）
    try:
        return webdriver.Edge()
    except Exception:
        pass
    # 尝试 Firefox
    try:
        return webdriver.Firefox()
    except Exception:
        pass
    return None
driver = setup_driver_alternative()
if driver:
    driver.get("https://httpbin.org/html")
    driver.quit()

'''在尝试过后，先用着edge浏览器来，不要追求完美，而要追求能用就行。'''