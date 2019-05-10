# Scraping Coupon Project - Backend.

Status: **In Development**

## Startup Guide

Activate virtualenv and install all the packages
```
$ cd coupon2.0
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run scrapyd for runnign spiders
```
$ cd scrapy_app
$ scrapyd
```

Open new tab and run scraping script to start crawling
```
$ cd ..
$ python manage.py runscript start_crawling
```