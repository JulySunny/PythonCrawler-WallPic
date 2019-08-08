# -*- coding: utf-8 -*-
import scrapy
import copy
from netbianSpider.items import NetbianspiderItem
import logging


class NetbianSpider(scrapy.Spider):
    """www.netbian.com图片爬虫"""
    name = 'netbian'
    allowed_domains = ['netbian.com']
    # 起始爬取的url--风景壁纸
    start_urls = ['http://www.netbian.com/dongman/']

    def parse(self, response):
        """图片分组"""
        detail_list = response.xpath("//div[@class='list']/ul/li")
        for detail in detail_list:
            item = NetbianspiderItem()
            # 每个图片的详情页
            detail_page = detail.xpath("./a/@href").extract_first()
            if detail_page is not None:
                detail_page = "http://www.netbian.com" + detail_page
                # print("detail_page::::::::::%s" % detail_page)
                yield scrapy.Request(
                        detail_page,
                        callback=self.parse_detail_page,
                        meta={"item": copy.deepcopy(item)}
                )
        # 构建下一页url
        exist = response.xpath("//div[@class='page']/a[@class='prev']//text()").extract() # 获取所有的a标签
        # print(exist)
        next_url=""
        if len(exist) == 2:
            # 如果有上一页和下一页 ,取下一页
            next_url=response.xpath("//div[@class='page']/a[@class='prev'][2]/@href").extract_first()
            next_url = "http://www.netbian.com" + next_url
        elif len(exist)==1 and response.xpath("//div[@class='page']/a[@class='prev']/text()").extract_first()=="下一页>":
            # 如果有仅有下一页,取下一页
            next_url=response.xpath("//div[@class='page']/a[@class='prev']/@href").extract_first()
            next_url = "http://www.netbian.com" + next_url
        print("next_url================%s" %next_url)
        yield scrapy.Request(
                # copy.deepcopy(next_url),
                next_url,
                callback=self.parse
                )
    def parse_detail_page(self, response):
        """图片详情页解析"""
        item = response.meta["item"]
        # 获取下载页href-相对路径
        download_page = response.xpath("//div[@class='pic-down']/a/@href").extract_first()
        # 绝对路径
        if download_page is not None:
            download_page = "http://www.netbian.com" + download_page
            # print("download_page:::::%s" % download_page)
            yield scrapy.Request(
                    download_page,
                    callback=self.parse_download_page,
                    # 深拷贝 继续传递
                    meta={"item": copy.deepcopy(item)}
            )

    def parse_download_page(self, response):
        """图片下载页解析,并传递下载URL到PIPLINE"""
        item = response.meta["item"]
        target_page = response.xpath("//table[@id='endimg']/tr/td/a/img/@src").extract_first()
        item["down_url"] = target_page
        logging.warning(item)
        yield item
