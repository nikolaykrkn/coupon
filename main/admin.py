from django.contrib import admin
from .models import Retailer, CouponSite, CouponItem


admin.site.register(Retailer)
admin.site.register(CouponSite)

class CouponItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'promo_code', 'expires_at', 'retailer', 'status', 'last_verified_date')
	list_filter = ('status', )
admin.site.register(CouponItem, CouponItemAdmin)