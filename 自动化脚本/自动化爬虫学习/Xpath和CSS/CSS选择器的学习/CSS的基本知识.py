'''
选择器 {
    属性: 值;
    属性: 值;
}
'''

我来逐行详细讲解这段爬虫代码：

## 导入库部分
```python
from bs4 import BeautifulSoup
import requests

```
- ** 第1行 **：从
`bs4`
库导入
`BeautifulSoup`
类，这是HTML / XML解析器
- ** 第2行 **：导入
`requests`
库，用于发送HTTP请求获取网页内容

## 获取网页内容
```python
response = requests.get('https://example.com')
```
- ** 第5行 **：使用
`requests.get()`
方法向
`https: // example.com
`发送GET请求
- 返回一个
`Response`
对象，包含服务器响应的所有信息（状态码、头信息、内容等）

```python
soup = BeautifulSoup(response.content, 'html.parser')
```
- ** 第6行 **：
- `response.content`：获取响应的二进制内容（适合HTML解析）
- `BeautifulSoup(..., 'html.parser')`：使用Python内置的HTML解析器创建BeautifulSoup对象
- `soup`
对象现在包含了整个网页的DOM结构，可以用各种方法进行查询

## 使用CSS选择器提取数据

### 提取所有链接
```python
links = soup.select('a')
```
- ** 第9行 **：使用CSS选择器
`'a'`
选择页面中所有的
` < a > `标签（链接）
- `soup.select()`
返回一个包含所有匹配元素的列表

```python
for link in links:
    print(link.get('href'))
```
- ** 第10 - 11
行 **：
- 遍历所有找到的链接元素
- `link.get('href')`：获取每个链接的
`href`
属性值（即链接地址）
- 打印出所有链接URL

### 提取特定class的元素
```python
articles = soup.select('.article')
```
- ** 第14行 **：使用CSS类选择器
`'.article'`
选择所有class包含
`article`
的元素
- 注意：类选择器前面有
`.
`符号

```python
for article in articles:
    title = article.select_one('h2').text
    print(title)
```
- ** 第15 - 17
行 **：
- 遍历所有class为
`article`
的元素
- `article.select_one('h2')`：在每个article元素内部使用元素选择器
`'h2'`
查找第一个
` < h2 > `标签
- `.text
`：获取该元素的文本内容（去除HTML标签）
- 打印文章标题

** 注意 **：这里有个潜在问题 - 如果某个article中没有h2标签，`article.select_one('h2')`
会返回
`None`，调用
`.text
`会报错。更安全的写法：
```python
title_element = article.select_one('h2')
if title_element:
    print(title_element.text)
```

### 提取属性包含特定值的元素
```python
images = soup.select('img[src*="logo"]')
```
- ** 第20行 **：使用属性选择器
`img[src *= "logo"]`
- `img`：选择所有
` < img > `标签
- `[src *= "logo"]`：选择
`src`
属性值中包含
"logo"
字符串的图片
- ` *= `是
"包含"
操作符

```python
for img in images:
    print(img['src'])
```
- ** 第21 - 22
行 **：
- 遍历所有匹配的图片元素
- `img['src']`：直接通过字典方式获取
`src`
属性值
- 打印所有包含
"logo"
的图片URL

## 完整代码重写（带错误处理）

```python
from bs4 import BeautifulSoup
import requests

try:
    # 获取网页内容
    response = requests.get('https://example.com', timeout=10)
    response.raise_for_status()  # 如果请求失败会抛出异常

    # 解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    print("=== 所有链接 ===")
    # 选择所有链接
    links = soup.select('a')
    for link in links:
        href = link.get('href')
        if href:  # 确保href不为空
            print(href)

    print("\n=== 文章标题 ===")
    # 选择特定class的元素
    articles = soup.select('.article')
    for article in articles:
        # 安全地获取标题
        title_element = article.select_one('h2')
        if title_element and title_element.text.strip():
            print(title_element.text.strip())

    print("\n=== Logo图片 ===")
    # 选择属性包含特定值的元素
    images = soup.select('img[src*="logo"]')
    for img in images:
        src = img.get('src')
        if src:
            print(src)

except requests.RequestException as e:
    print(f"请求错误: {e}")
except Exception as e:
    print(f"解析错误: {e}")
```

## 关键知识点总结

1. ** `soup.select()` ** - 返回所有匹配元素的列表
2. ** `soup.select_one()` ** - 返回第一个匹配元素（找不到返回None）
3. ** `.get('属性名')
` ** - 安全获取元素属性值
4. ** `['属性名']` ** - 直接获取属性值（属性不存在会报错）
5. ** `.text
` ** - 获取元素的文本内容

这段代码展示了爬虫中最常见的三种数据提取场景：提取链接、提取结构化内容、提取特定资源。