import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import requests
import re
import json
import unicodedata


class CoucrawlerSpider(CrawlSpider):
    name = 'coucrawler'
    
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.retailer = kwargs.get('retailer')
        self.page_link = kwargs.get('page_link')
        super(CoucrawlerSpider, self).__init__(*args, **kwargs)
        
    def parse(self, response):
        session = requests.Session()
        res_session = session.get(self.url)
        target = session.get(self.page_link)
        soup = BeautifulSoup(target.text, 'html.parser')
        coupon = ''
        get_btns = soup.findAll('div', {'class': 'coupon-button'})
        for index, get_btn in enumerate(get_btns):
            item = {}
            if get_btn.text == 'Get coupon code':
                # param = re.sub(r'.*/', '', get_btn.a['href'])
                # page = session.get(self.page_url+"?c="+param)
                # soup_page = BeautifulSoup(page.text, 'html.parser')
                text = soup.find('script', type='text/javascript').text
                data = json.loads(text.split('=', 1)[-1][:-1])
                coupon_data = data["state"]["stores_slug"]["coupons"][index]
                coupon_code = coupon_data["code"]
                if coupon_code != '':
                    item['promo_code'] = coupon_code
                    item['retailer'] = self.retailer
                    item['title'] = coupon_data['title']
                    item['from'] = self.url
                    item['expires_at'] = coupon_data['endsAt']
                    yield item
