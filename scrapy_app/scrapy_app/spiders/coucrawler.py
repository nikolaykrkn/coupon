import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import requests
import re
import json
import unicodedata
from datetime import datetime
import logging


class CoucrawlerSpider(CrawlSpider):
    name = 'coucrawler'
    
    def __init__(self, *args, **kwargs):
        super(CoucrawlerSpider, self).__init__(*args, **kwargs)
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        # self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.retailer = kwargs.get('retailer')
        self.page_link = kwargs.get('page_link')
        self.start_urls = [self.scrape_url]
        
       
        
    def parse(self, response):
        for coupon in response.xpath('//div[not(@data-bucket="expired")]/ul[contains(@class, "offer-list")]/li/div[contains(@class, "offer-item")]'):
            if coupon.xpath('./@data-offer-type').extract_first() in ["code", "singleuse"]:
                code = coupon.xpath('./@data-clipboard-text').extract_first()

                if code:
                    item = {}
                    item['promo_code'] = coupon.xpath('./@data-clipboard-text').extract_first()
                    item['retailer'] = self.retailer
                    item['title'] = coupon.xpath('.//div[@class="offer-item-title"]/a/text()').extract_first()
                    item['from'] = self.url
                    expire_date = coupon.xpath(
                        './/p/strong[contains(text(), "End")]/../text() | .//p/strong[contains(text(), "Expire")]/../text()').re_first(r"(?:\d{1,4}/?){3}")
                    logging.info(expire_date)
                    if expire_date:
                        expire_dt_lst = [int(x) for x in expire_date.split('/')]
                        if expire_dt_lst[2] < 2000:
                            expire_dt_lst[2] += 2000
                        item['expires_at'] = datetime(expire_dt_lst[2], expire_dt_lst[0], expire_dt_lst[1])
                        logging.info(expire_date, expire_dt_lst[2], item['expires_at'])
                    else:
                        item['expires_at'] = None
                    yield item
        # session = requests.Session()
        # res_session = session.get(self.url)
        # target = session.get(self.page_link)
        # soup = BeautifulSoup(target.text, 'html.parser')
        # coupon = ''
        # get_btns = soup.findAll('div', {'class': 'coupon-button'})
        # for index, get_btn in enumerate(get_btns):
        #     item = {}
        #     if get_btn.text == 'Get coupon code':
        #         # param = re.sub(r'.*/', '', get_btn.a['href'])
        #         # page = session.get(self.page_url+"?c="+param)
        #         # soup_page = BeautifulSoup(page.text, 'html.parser')
        #         text = soup.find('script', type='text/javascript').text
        #         data = json.loads(text.split('=', 1)[-1][:-1])
        #         coupon_data = data["state"]["stores_slug"]["coupons"][index]
        #         coupon_code = coupon_data["code"]
        #         if coupon_code != '':
        #             item['promo_code'] = coupon_code
        #             item['retailer'] = self.retailer
        #             item['title'] = coupon_data['title']
        #             item['from'] = self.url
        #             item['expires_at'] = coupon_data['endsAt']
        #             yield item
