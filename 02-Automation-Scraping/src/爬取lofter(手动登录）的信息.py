from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

def lofter():
    options=Options()
# 反检测配置
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 模拟真实用户
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Edge(options=options)
    # 执行JavaScript移除webdriver属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    url="https://www.lofter.com/tag/%E8%AF%A1%E7%A7%98%E4%B9%8B%E4%B8%BBoc"
    driver.get(url)
    phone_input = driver.find_element(By.TAG_NAME, "input")
    phone_input.send_keys("13766397710")
    time.sleep(3)
    fa_song=driver.find_elements(By.NAME,'获取验证码')
#<div class="EuoSRSUNPbbLCCRQmAzIfQ== " aria-hidden="true">获取验证码</div>
#<div class="EuoSRSUNPbbLCCRQmAzIfQ== " aria-hidden="true">获取验证码</div>
    for b in fa_song:
         b.click()#发送验证码
#点击获取验证码后，会弹出一个验证窗口，目前这个问题还不知何解决。
#虽然手机验证码登录问题还是没有解决，但是send_keys()和click()方法已为我开启了一扇新的门。自动化操控浏览器的门。
    tong=driver.find_element(By.TAG_NAME,'circle')
    tong.click()#点击同意用户协议
#<button type="button" class="AaRSlfX5LcBgEqyHokS0hg== IWKkWSqHHfy16K39b0EUJQ== kbiv8yHlefNEThxFhRrfBQ==  hWICwaWdoLhCggGxnBgfhA==">注册/登录</button>
    lll=driver.find_element(By.TAG_NAME,'input')
#<input type="text" placeholder="请输入验证码" class="vFxkt-gwu3ZAU3IZDjRQAA== ChtAyXVasJoZuqW5nzuRlQ== " autocomplete="off" maxlength="6" value="">
    time.sleep(30)
    x=input('请尽快输入验证码：')
    lll.send_keys(x)#输入获取的验证码
    gggg=driver.find_element(By.CLASS_NAME,'AaRSlfX5LcBgEqyHokS0hg== IWKkWSqHHfy16K39b0EUJQ== kbiv8yHlefNEThxFhRrfBQ==  hWICwaWdoLhCggGxnBgfhA==')
#<button type="button" class="AaRSlfX5LcBgEqyHokS0hg== IWKkWSqHHfy16K39b0EUJQ== kbiv8yHlefNEThxFhRrfBQ==  hWICwaWdoLhCggGxnBgfhA==">注册/登录</button>
    gggg.click()#点击登录按钮。
    html=driver.page_source
#soup=BeautifulSoup(html,'html,parser')
#l=soup.find_all('h2')
#book_title=[]
#for v in l:
   # book_title.append(v.string)
#f=str(book_title)
#with open('./在lofter爬取的诡秘同人文书名.txt','w',encoding='utf-8') as g:
#    g.write(f)
'''还是没有成功，因为在click发送验证码的按钮后，会出现一个用来验明click按钮的是人还是机器的窗口。'''









