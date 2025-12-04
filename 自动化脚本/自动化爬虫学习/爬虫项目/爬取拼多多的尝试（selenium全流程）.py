from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
def pa_ping_duo_duo():
    options=Options()
#options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Edge(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url='https://mobile.pinduoduo.com/login.html?from=https%3A%2F%2Fmobile.pinduoduo.com%2Fsearch_result.html%3Fsearch_key%3D%25E9%259A%258F%25E8%25BA%25ABwifi%26search_met_track%3Dhistory%26search_type%3Dgoods%26source%3Dindex%26options%3D3%26refer_search_met_pos%3D0%26refer_page_el_sn%3D99887%26refer_page_name%3Dsearch_result%26refer_page_id%3D10015_1760089559270_3bzsl9txn8%26refer_page_sn%3D10015&refer_page_name=search_result&refer_page_id=10015_1760089562057_8be7i9z4k3&refer_page_sn=10015'
    driver.get(url)
    time.sleep(1)
    html=driver.page_source
#print(html)
#点击手机登录按钮。
    an=driver.find_element(By.TAG_NAME,'span')
    an.click()
    phone_input = driver.find_element(By.ID, "user-mobile")
    phone_input.send_keys("13766397710")
#send_keys()方法是什么意思？大概是输入。
#<input type="tel" id="user-mobile" placeholder="手机号码" value="">
    send_btn = driver.find_element(By.ID, "code-button")
    send_btn.click()#点击发送验证码。
#<input type="tel" id="input-code" placeholder="验证码">
#<button type="button" id="code-button" data-active="ghost-red" disabled="">发送验证码</button>
    time.sleep(30)#有三十秒的时间手动输入验证码。
    yan=driver.find_element(By.ID,'input-code')
    x=input('请尽快输入发送到手机上的验证码：')
    yan.send_keys(x)
    tong_yi=driver.find_elements(By.TAG_NAME,'i')
    for c in tong_yi:
         c.click()#点击同意用户协依按纽。
#<label class="agreement-label" for="agreement">同意</label>
# 点击登录按钮
    login_btn = driver.find_element(By.ID, "submit-button")
    login_btn.click()
#<button type="submit" data-active="red" id="submit-button">登录</button>
    time.sleep(5)
# 保存cookies供后续使用
#cookies = driver.get_cookies()
pa_ping_duo_duo()
'''没有取得理想的效果，具体表现在登录后提示网络繁满。'''
'''和“关于爬取拼多多的尝试.py”一样的问题。'''