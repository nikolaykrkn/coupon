import json
from datetime import datetime
from django.db import models
from django.utils import timezone

COUPON_STATUS_CHOICES = (
    ("unverified", "unverified"),
    ("valid", "valid"),
    ("invalid", "invalid"),
    ("expired", "expired")
)

TASK_STATUS_CHOICES = (
    ("started", "started"),
    ("pending", "pending"),
    ("running", "running"),
    ("finished", "finished")
)


class CouponSite(models.Model):
    title = models.CharField(max_length=50, null=True)
    link = models.CharField(max_length=50, null=True)
    page_link = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.page_link


class Retailer(models.Model):
    title = models.CharField(max_length=50, null=True)
    slug_id = models.CharField(max_length=50, null=True)
    link = models.CharField(max_length=50, null=True)
    coupon_sites = models.ManyToManyField(CouponSite)

    def __str__(self):
        return self.title


class CouponItem(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    promo_code = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200, null=True)
    last_verified_date = models.DateTimeField(null=True)
    expires_at = models.DateTimeField(null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=COUPON_STATUS_CHOICES, default="unverified")
    coupon_from = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "scrapped coupon"
    
    def to_dict(self):
        data = {
            'promo_code': self.promo_code,
            'last_verified': self.get_last_verified_by_min,
            'retailer': self.retailer.title,
            'coupon': self.retailer.coupon_site.title
        }
        return data

    def get_last_verified_by_min(self):
        now = datetime.now()
        diff = (now - self.last_verified_date).total_seconds / 60.0
        return "Tested {} mins ago".format(round(diff))

    def __str__(self):
        return self.promo_code


class CrawlTask(models.Model):
    task_id = models.CharField(max_length=100, null=True)
    unique_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=10, choices=TASK_STATUS_CHOICES)

    def __str__(self):
        return self.task_id + self.status
