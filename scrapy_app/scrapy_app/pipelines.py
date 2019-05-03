# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from main.models import CouponItem, Retailer, CrawlSite
import json

class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def process_item(self, item, spider):
        new_item = CouponItem()
        new_item.unique_id = self.unique_id
        new_item.promo_code = item['promo_code']
        crawlsite = CrawlSite.objects.get(title='groupon.com')
        retailer = Retailer.objects.get(title='tjmaxx.tjx.com')
        new_item.retailer = retailer
        new_item.crawlsite = crawlsite
        new_item.save()
        return item