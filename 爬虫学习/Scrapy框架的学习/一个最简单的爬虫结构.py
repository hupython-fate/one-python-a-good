import scrapy


class SimpleSpider(scrapy.Spider):
    name = "simple"  # 爬虫的唯一标识
    start_urls = ["http://books.toscrape.com"]  # 起始网址

    def parse(self, response):
        # 这个函数处理网页响应
        title = response.css('title::text').get()
        yield {
            'page_title': title,
            'url': response.url
        }