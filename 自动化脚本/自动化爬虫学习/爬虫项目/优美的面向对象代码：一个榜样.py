from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import time
import random


class QidianAutoSearch:
    def __init__(self):
        self.driver = None
        self.initial_url = None

    def setup_driver(self):
        """配置浏览器驱动"""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Edge(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def navigate_to_page(self, url):
        """导航到指定页面"""
        print(f"正在导航到: {url}")
        self.driver.get(url)
        self.initial_url = url
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("页面加载完成")

    def simulate_human_typing(self, element, text):
        """模拟人类输入（带随机延迟）"""
        actions = ActionChains(self.driver)
        actions.click(element)
        actions.pause(random.uniform(0.2, 0.5))

        for char in text:
            actions.send_keys(char)
            actions.pause(random.uniform(0.1, 0.3))  # 随机输入间隔

        actions.perform()

    def find_and_click_search(self):
        """查找并点击搜索按钮"""
        print("寻找搜索按钮...")

        # 可能的搜索按钮选择器
        selectors = [
            '.lbf-icon-search',  # 搜索图标
            '.search-btn',  # 搜索按钮
            'button[type="submit"]',  # 提交按钮
            'input[type="submit"]',  # 提交输入框
            '.lbf-panel-submit',  # 面板提交按钮
            'i[class*="search"]',  # 包含search的图标
            'span[class*="search"]',  # 包含search的span
        ]

        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    print(f"找到搜索按钮: {selector}")
                    element.click()
                    return True
            except:
                continue

        return False

    def wait_for_redirect(self, timeout=10):
        """等待页面跳转"""
        print("等待页面跳转...")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_changes(self.initial_url)
            )
            new_url = self.driver.current_url
            print(f"✓ 页面跳转成功!")
            print(f"新URL: {new_url}")
            return new_url
        except:
            print("✗ 页面未发生跳转")
            return self.driver.current_url

    def search_by_direct_url(self, keyword):
        """通过直接URL进行搜索（备用方案）"""
        encoded_keyword = quote(keyword.encode('utf-8'))
        search_url = f'https://www.qidian.com/search?kw={encoded_keyword}'
        print(f"使用直接搜索URL: {search_url}")
        self.driver.get(search_url)
        return self.driver.current_url

    def search_by_interaction(self, keyword):
        """通过页面交互进行搜索"""
        print(f"开始搜索: {keyword}")

        # 等待搜索框加载
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 's-box'))
            )
            print("✓ 搜索框已就绪")
        except:
            print("✗ 无法找到搜索框")
            return None

        # 清空并输入搜索词
        search_box.clear()
        self.simulate_human_typing(search_box, keyword)
        print("✓ 已输入搜索关键词")

        # 方法1: 尝试点击搜索按钮
        if self.find_and_click_search():
            return self.wait_for_redirect()

        # 方法2: 尝试回车键
        print("尝试使用回车键...")
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        result_url = self.wait_for_redirect(5)
        if result_url != self.initial_url:
            return result_url

        # 方法3: 通过JavaScript触发搜索
        print("尝试JavaScript触发...")
        try:
            self.driver.execute_script("""
                var searchBox = document.getElementById('s-box');
                var event = new Event('input', { bubbles: true });
                searchBox.dispatchEvent(event);

                // 尝试找到并点击搜索按钮
                var searchBtns = document.querySelectorAll('.lbf-icon-search, .search-btn');
                for (var btn of searchBtns) {
                    if (btn.offsetParent !== null) { // 元素可见
                        btn.click();
                        break;
                    }
                }
            """)
            time.sleep(2)
            result_url = self.wait_for_redirect(5)
            if result_url != self.initial_url:
                return result_url
        except Exception as e:
            print(f"JavaScript触发失败: {e}")

        return None

    def auto_search(self, start_url, keyword):
        """自动化搜索主流程"""
        print("=" * 50)
        print("启动自动化搜索程序")
        print("=" * 50)

        # 设置驱动
        self.setup_driver()

        try:
            # 导航到起始页面
            self.navigate_to_page(start_url)

            # 方法1: 通过页面交互搜索
            print("\n--- 方法1: 页面交互搜索 ---")
            result_url = self.search_by_interaction(keyword)

            # 方法2: 如果交互失败，使用直接URL
            if not result_url or result_url == self.initial_url:
                print("\n--- 方法2: 直接URL搜索 ---")
                result_url = self.search_by_direct_url(keyword)

            # 输出最终结果
            print("\n" + "=" * 50)
            print("自动化搜索完成!")
            print(f"起始URL: {start_url}")
            print(f"搜索关键词: {keyword}")
            print(f"最终URL: {result_url}")
            print("=" * 50)

            return result_url

        except Exception as e:
            print(f"程序执行出错: {e}")
            return None
        finally:
            # 保持浏览器打开以便查看结果
            print("\n浏览器将保持打开状态，请手动关闭...")
            input("按回车键退出程序...")
            if self.driver:
                self.driver.quit()


# 使用示例
if __name__ == "__main__":
    # 创建自动化搜索实例
    auto_searcher = QidianAutoSearch()

    # 配置搜索参数
    start_url = "https://www.qidian.com/all/chanId14300-orderId11/"
    search_keyword = "诡秘之主"

    # 执行自动化搜索
    final_url = auto_searcher.auto_search(start_url, search_keyword)