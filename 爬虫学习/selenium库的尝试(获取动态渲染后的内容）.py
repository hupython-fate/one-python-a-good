from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
url='https://movie.douban.com/chart'
driver.get(url)
print(driver.page_source)