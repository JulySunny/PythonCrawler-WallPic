# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib.request


class NetbianspiderPipeline(object):
    def process_item(self, item, spider):
        if not os.path.exists("./dongman"):
            os.mkdir("./dongman")
        # 获取到的item
        url = item["down_url"]
        if url is not None:
            print("url::::::%s" % url)
            name = str(url).split("/")[-1]
            with urllib.request.urlopen(url, timeout=30) as response, open("./dongman/" + name, "wb") as f:
                f.write(response.read())
                f.flush()
                f.close()
        return item
