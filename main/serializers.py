from rest_framework import serializers
from .models import CouponItem, Retailer, CouponSite


class CouponItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponItem
        fields = '__all__'


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = '__all__'


class CrawlSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponSite
        fields = '__all__'