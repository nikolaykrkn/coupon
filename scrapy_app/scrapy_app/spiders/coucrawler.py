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
        import pdb; pdb.set_trace()
        
        self.domain = kwargs.get('domain')
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.coupon_page = kwargs.get('coupon_page')
        self.page_url = self.url + self.coupon_page
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        super(CoucrawlerSpider, self).__init__(*args, **kwargs)
        
    def parse(self, response):
        item = {}
        session = requests.Session()
        res_session = session.get(self.url)
        target = session.get(self.page_url)
        soup = BeautifulSoup(target.text, 'html.parser')
        coupon = ''
        get_btns = soup.findAll('div', {'class': 'coupon-button'})
        for index, get_btn in enumerate(get_btns):
            if get_btn.text == 'Get coupon code':
                param = re.sub(r'.*/', '', get_btn.a['href'])
                page = session.get(self.page_url+"?c="+param)
                soup_page = BeautifulSoup(page.text, 'html.parser')
                text = soup_page.find('script', type='text/javascript').text
                data = json.loads(text.split('=', 1)[-1][:-1])
                coupon = data["state"]["stores_slug"]["coupons"][1]["code"]
                if coupon != '':
                    item['promo_code'] = coupon
                    item['title'] = self.title
                    break

        return item
