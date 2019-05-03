from django.contrib import admin
from .models import Retailer, CrawlSite, CouponItem


admin.site.register(Retailer)
admin.site.register(CrawlSite)
admin.site.register(CouponItem)