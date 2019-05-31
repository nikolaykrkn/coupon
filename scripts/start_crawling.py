from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from main.models import Retailer
from scrapyd_api import ScrapydAPI

import time

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) # check if url format is valid
    except ValidationError:
        return False

    return True


def run():
    print("=====================crawling started==================")
    time.sleep(1)

    retailers = Retailer.objects.all()
    for retailer in retailers:
        coupon_sites = retailer.coupon_sites.all()
        for coupon_site in coupon_sites:
            url = coupon_site.link
            domain = urlparse(url).netloc # parse the url and extract the domain
            unique_id = str(uuid4()) # create a unique ID. 
            retailer_title = retailer.title
            page_link = coupon_site.page_link

            scrape_url = coupon_site.page_link + retailer.slug_id

            # This is the custom settings for scrapy spider. 
            # We can send anything we want to use it inside spiders and pipelines. 
            # I mean, anything
            settings = {
                'unique_id': unique_id, # unique ID for each record for DB
            }

            # Here we schedule a new crawling task from scrapyd. 
            # Notice that settings is a special argument name. 
            # But we can pass other arguments, though.
            # This returns a ID which belongs and will be belong to this task
            
            task = scrapyd.schedule('default', 'coucrawler', 
                settings=settings, url=url, domain=domain, retailer=retailer_title, page_link=page_link, scrape_url=scrape_url)