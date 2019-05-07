# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from main.models import CouponItem, Retailer, CouponSite

class ScrapyAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def process_item(self, item, spider):
        retailer = Retailer.objects.get(title=item['title'])
        new_item, created = CouponItem.objects.update_or_create(
            retailer=retailer,
            defaults = {
                'promo_code': item['promo_code']
            },
        )
        return item