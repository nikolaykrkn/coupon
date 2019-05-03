import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import requests
import unicodedata


class CoucrawlerSpider(CrawlSpider):
    name = 'coucrawler'
    
    def __init__(self, *args, **kwargs):
        self.url = 'https://groupon.com' # kwargs.get('url')
        self.sub_url = '/deals/cpn-tj-maxx'
        self.domain = 'groupon.com' # kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        self.sub_form = '//a[contains(@class, "signin")]'
        self.collapsed_span = '//span[text()="Coupon Code"]'
        self.see_code_btn = '//a[text()="See Coupon Code"]'
        self.coupon_code = '//div[contains(@style, "font-size: 20px")]'

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        
        self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        # CoucrawlerSpider.rules = [
        #    Rule(LinkExtractor(unique=True), callback='parse_item'),
        # ]
        super(CoucrawlerSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = {}
        self.driver.get(response.url + self.sub_url)

        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.sub_form)))
            self.driver.find_element(By.XPATH, self.sub_form).click()
        except TimeoutException:
            print("Timeout exception!")
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.collapsed_span)))
            self.driver.find_element(By.XPATH, self.collapsed_span).click()
        except TimeoutException:
            print("Timeout exception!")
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.see_code_btn)))
            self.driver.find_element(By.XPATH, self.see_code_btn).click()
        except TimeoutException:
            print("Timeout exception!")
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.coupon_code)))
            import pdb; pdb.set_trace()
            item['promo_code'] = self.driver.find_element_by_xpath(self.coupon_code).text
        except TimeoutException:
            print("Timeout exception!")
        
        return item

    def parse_second(self, response):
        self.driver.close()
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        url_session = requests.Session()
        res_session = url_session.get("https://"+self.domain)
        target = url_session.get(response.url)
        res = unicodedata.normalize('NFKD', target.text).encode('ascii','ignore')
        html_parsed = HtmlResponse(url="html response", body=res)

        return item
