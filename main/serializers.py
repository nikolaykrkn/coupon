from rest_framework import serializers
from .models import CouponItem, Retailer, CouponSite


class CouponItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponItem
        fields = ('promo_code', 'title', 'retailer', 'last_verified_date', 'status', 'coupon_from', 'expires_at',)


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = '__all__'


class CrawlSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponSite
        fields = '__all__'