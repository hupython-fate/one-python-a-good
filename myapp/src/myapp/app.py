"""
一个把自己写的爬虫程序通用化的尝试，用途是输入一个网址，就会下载这个网址对应页面的图片。
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import requests
from bs4 import BeautifulSoup
import os
import time
import threading
from urllib.parse import urljoin, urlparse


class ImageDownloaderApp(toga.App):
    def startup(self):
        # 创建主窗口
        self.main_window = toga.MainWindow(title=self.formal_name)

        # 创建主容器
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # URL 输入区域
        url_label = toga.Label("输入图片网页URL:", style=Pack(padding=(0, 0, 5, 0)))
        self.url_input = toga.TextInput(
            placeholder="例如: https://example.com",
            style=Pack(padding=5, flex=1)
        )

        # 下载选项区域
        options_label = toga.Label("下载选项:", style=Pack(padding=(10, 0, 5, 0)))

        # 文件夹名称输入
        folder_box = toga.Box(style=Pack(direction=ROW, padding=5))
        folder_label = toga.Label("文件夹名:", style=Pack(padding=(0, 5, 0, 0)))
        self.folder_input = toga.TextInput(
            value="爬到的图集",
            style=Pack(padding=5, flex=1)
        )
        folder_box.add(folder_label)
        folder_box.add(self.folder_input)

        # 控制按钮
        button_box = toga.Box(style=Pack(direction=ROW, padding=10))
        self.download_btn = toga.Button(
            "开始下载图片",
            on_press=self.start_download,
            style=Pack(padding=5, flex=1)
        )
        self.cancel_btn = toga.Button(
            "取消下载",
            on_press=self.cancel_download,
            style=Pack(padding=5, flex=1),
            enabled=False
        )
        button_box.add(self.download_btn)
        button_box.add(self.cancel_btn)

        # 进度显示
        self.progress_bar = toga.ProgressBar(max=100, value=0, style=Pack(padding=5))

        # 状态显示
        self.status_label = toga.Label(
            "准备就绪",
            style=Pack(padding=10, text_align="center")
        )

        # 日志输出
        self.log_output = toga.MultilineTextInput(
            readonly=True,
            style=Pack(padding=5, flex=1, height=200)
        )

        # 添加所有部件到主容器
        main_box.add(url_label)
        main_box.add(self.url_input)
        main_box.add(options_label)
        main_box.add(folder_box)
        main_box.add(button_box)
        main_box.add(self.progress_bar)
        main_box.add(self.status_label)
        main_box.add(self.log_output)

        # 设置窗口内容
        self.main_window.content = main_box
        self.main_window.show()

        # 下载控制变量
        self.is_downloading = False
        self.current_thread = None

    def log_message(self, message):
        """添加消息到日志"""
        current_time = time.strftime("%H:%M:%S")
        log_entry = f"[{current_time}] {message}\n"
        self.log_output.value += log_entry
        # 自动滚动到底部
        self.log_output.scroll_to_bottom()

    def update_progress(self, value, max_value=100):
        """更新进度条"""
        if max_value > 0:
            progress = (value / max_value) * 100
            self.progress_bar.value = min(progress, 100)

    def start_download(self, widget):
        """开始下载图片"""
        url = self.url_input.value.strip()
        folder_name = self.folder_input.value.strip()

        if not url:
            self.status_label.text = "错误: 请输入URL"
            return

        if not folder_name:
            folder_name = "爬到的图集"

        # 更新UI状态
        self.is_downloading = True
        self.download_btn.enabled = False
        self.cancel_btn.enabled = True
        self.status_label.text = "正在下载..."
        self.log_output.value = ""  # 清空日志
        self.progress_bar.value = 0

        # 在新线程中执行下载
        self.current_thread = threading.Thread(
            target=self.download_images,
            args=(url, folder_name)
        )
        self.current_thread.start()

    def cancel_download(self, widget):
        """取消下载"""
        self.is_downloading = False
        self.status_label.text = "下载已取消"
        self.log_message("用户取消了下载")
        self.download_btn.enabled = True
        self.cancel_btn.enabled = False

    def download_images(self, url, folder_name):
        """下载图片的主函数"""
        try:
            self.log_message(f"开始处理URL: {url}")

            # 获取网页内容
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            self.log_message("网页获取成功，开始解析图片链接...")

            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            img_tags = soup.find_all('img')

            # 提取图片URL
            img_urls = []
            for img in img_tags:
                src = img.get('src') or img.get('data-src')
                if src:
                    # 处理相对URL
                    if src.startswith('//'):
                        full_url = 'https:' + src
                    elif src.startswith('/'):
                        full_url = urljoin(url, src)
                    elif not src.startswith(('http://', 'https://')):
                        full_url = urljoin(url, src)
                    else:
                        full_url = src

                    # 过滤掉一些常见的不需要的图片
                    if not any(ignore in full_url.lower() for ignore in ['pixel', 'tracking', 'analytics', 'icon']):
                        img_urls.append(full_url)

            self.log_message(f"找到 {len(img_urls)} 个可能的图片链接")

            if not img_urls:
                self.log_message("未找到任何图片链接")
                self.finalize_download(0, 0)
                return

            # 创建下载目录
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # 下载图片
            session = requests.Session()
            session.headers.update(headers)

            successful_downloads = 0
            for i, img_url in enumerate(img_urls):
                if not self.is_downloading:
                    break

                self.log_message(f"正在下载第 {i + 1}/{len(img_urls)} 张图片")
                self.update_progress(i, len(img_urls))

                try:
                    img_response = session.get(img_url, timeout=5)
                    if img_response.status_code == 200:
                        # 确定文件扩展名
                        content_type = img_response.headers.get('content-type', '')
                        if 'jpeg' in content_type or 'jpg' in content_type:
                            ext = '.jpg'
                        elif 'png' in content_type:
                            ext = '.png'
                        elif 'gif' in content_type:
                            ext = '.gif'
                        else:
                            # 从URL推断扩展名
                            parsed_url = urlparse(img_url)
                            path = parsed_url.path.lower()
                            if '.jpg' in path or '.jpeg' in path:
                                ext = '.jpg'
                            elif '.png' in path:
                                ext = '.png'
                            elif '.gif' in path:
                                ext = '.gif'
                            else:
                                ext = '.jpg'  # 默认

                        filename = os.path.join(folder_name, f'图片_{i + 1}{ext}')
                        with open(filename, 'wb') as f:
                            f.write(img_response.content)

                        successful_downloads += 1
                        self.log_message(f"✓ 成功保存: {filename}")
                    else:
                        self.log_message(f"✗ 下载失败，状态码: {img_response.status_code}")

                except Exception as e:
                    self.log_message(f"✗ 下载出错: {str(e)}")

                time.sleep(0.5)  # 防止请求过快

            self.finalize_download(successful_downloads, len(img_urls))

        except Exception as e:
            self.log_message(f"错误: {str(e)}")
            self.status_label.text = f"错误: {str(e)}"
            self.download_btn.enabled = True
            self.cancel_btn.enabled = False

    def finalize_download(self, successful, total):
        """完成下载后的清理工作"""
        if self.is_downloading:
            self.status_label.text = f"下载完成! 成功: {successful}/{total}"
            self.log_message(f"下载完成! 成功下载 {successful}/{total} 张图片")
        else:
            self.status_label.text = f"下载中断! 成功: {successful}/{total}"

        self.progress_bar.value = 100
        self.download_btn.enabled = True
        self.cancel_btn.enabled = False
        self.is_downloading = False


def main():
    return ImageDownloaderApp()


if __name__ == '__main__':
    main().main_loop()

