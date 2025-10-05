import requests
import os
from urllib.parse import urljoin
'''urllib 是一个包

parse 是 urllib 包中的一个模块

urljoin 是 urllib.parse 模块中的一个函数

功能：将相对URL转换为绝对URL'''
from bs4 import BeautifulSoup


def download_images(url, save_dir='images'):
    """下载页面中的所有图片"""
    #'''save_dir='images' 是默认参数'''
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
#BeautifulSoup(response.text, 'html.parser')

#BeautifulSoup 是一个类

#这里是在创建BeautifulSoup类的实例（对象）

#response.text 是 Response 对象的属性（包含网页HTML）

#'html.parser' 指定使用Python内置的HTML解析器



    # 找到所有图片标签
    img_tags = soup.find_all('img')#返回：ResultSet 对象（类似列表）

    downloaded_count = 0
    for img in img_tags:
        img_url = img.get('src')
        #img.get('src')
#img 是 Tag 类的实例（代表一个HTML标签）
#get 是 Tag 对象的方法
#功能：获取标签的 src 属性值（图片URL）
        if not img_url:
            continue#如果条件为真，那么就跳过余下的语句，重新开始下一轮循环。

        # 处理相对URL
        img_url = urljoin(url, img_url)#urljoin 是 urllib.parse 模块中的一个函数
        # 功能：将相对URL转换为绝对URL
        # 功能：将基础URL和相对URL组合成完整URL
        try:
            # 下载图片
            img_response = requests.get(img_url, headers=headers, timeout=10)
            '''再次使用
            requests.get函数下载图片
            timeout = 10
            设置超时时间为10秒'''
            if img_response.status_code == 200:
                # 从URL提取文件名
                filename = os.path.basename(img_url)
                #basename 是 os.path 模块中的函数。功能：从URL中提取文件名。
                if not filename or '.' not in filename:
                    filename = f'image_{downloaded_count}.jpg'

                filepath = os.path.join(save_dir, filename)

                # 保存图片
                with open('./一些爬到照片', 'wb') as f:
                    f.write(img_response.content)

                print(f'下载成功: {filename}')
                downloaded_count += 1

        except Exception as e:
            print(f'下载失败 {img_url}: {e}')

    print(f'总共下载了 {downloaded_count} 张图片')


# 使用示例
url='https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=utf8&sa=vs_ala_img&fr=ala&ala=1&alatpl=normal&pos=3&dyTabStr=MCwzLDEsMiwxMyw3LDYsNSwxMiw5&word=%E8%91%A3%E9%A6%99%E5%9B%BE&lid=ee58b8bc03fc9099&topic=%E8%91%A3%E9%A6%99%E5%9B%BE'
download_images(url)