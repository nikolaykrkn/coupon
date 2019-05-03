import json
from datetime import datetime
from django.db import models
from django.utils import timezone

STATUS_CHOICES = (
    ("valid", "Valid"),
    ("invalid", "Invalid"),
    ("expired", "Expired")
)


class Retailer(models.Model):
    title = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title


class CrawlSite(models.Model):
    title = models.CharField(max_length=50, null=True)
    path = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title


class CouponItem(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    promo_code = models.CharField(max_length=100, null=True)
    last_verified_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    retailer = models.OneToOneField(Retailer, on_delete=models.CASCADE, null=True)
    crawlsite = models.OneToOneField(CrawlSite, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "scrapped Coupon"
    
    @property
    def to_dict(self):
        data = {
            'promo_code': self.promo_code,
            'last_verified': self.get_last_verified_by_min
        }
        return data

    @property
    def get_last_verified_by_min(self):
        now = datetime.now()
        diff = (now - self.last_verified_date).total_seconds / 60.0
        return "Tested {} mins ago".format(round(diff))

    def __str__(self):
        return self.promo_code