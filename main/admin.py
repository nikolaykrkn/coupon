from django.contrib import admin
from .models import Retailer, CouponSite, CouponItem


admin.site.register(Retailer)
admin.site.register(CouponSite)
admin.site.register(CouponItem)