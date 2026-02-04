import requests
import re

url = "https://httpbin.org/xml"
response = requests.get(url)
xml_text = response.text

print("原始XML数据:")
print(xml_text)

pattern = r'type="(.*?)"'
matches = re.findall(pattern, xml_text)

if matches:
    slide_type = matches[0]  # 获取第一个匹配结果
    print(f"\n提取成功！第一个slide的type是: {slide_type}")
else:
    print("\n未找到目标内容。")