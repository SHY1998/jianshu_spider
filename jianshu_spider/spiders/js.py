# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath(".//h1[@class='_1RuRku']/text()").get()
        avatar = response.xpath(".//a[@class='_1OhGeD']/img/@src").get()
        # article = response.xpath(".//article[@class='_2rhmJa']/p/text()").get()
        author = response.xpath(".//span[@class='_22gUMi']/text()").get()
        time = response.xpath(".//time/text()").get()
        url  = response.url
        url1 = url.split("?")[0]
        article_id = url1.split('/')[-1]
        content = response.xpath(" .//article[@class='_2rhmJa']").get()
        word_count =response.xpath(".//div[@class='s-dsoj']/span[1]/text()").get()
        like_count = response.xpath(".//span[@class='_1LOh_5']/text()").get()
        read_count = response.xpath(".//div[@class='s-dsoj']/span[2]/text()").get()
        subjects = ",".join(response.xpath(".//div[@class='_2Nttfz']/a/span/text()").getall())
        item = ArticleItem(
            title=title,
            avatar=avatar,
            pub_time=time,
            origin_url = response.url,
            article_id=article_id,
            author=author,
            content=content,
            subjects = subjects,
            word_count = word_count,
            like_count = like_count,
            read_count = read_count
        )
        yield item



