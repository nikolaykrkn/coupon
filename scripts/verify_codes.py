from main.models import CouponItem, Retailer
import requests
import json
from datetime import datetime
from django.utils import timezone

import time

def run():

    for retailer in (Retailer.objects.all()):
        now = timezone.now()
        coupons = CouponItem.objects.filter(retailer=retailer, status__in=["unverified", "valid"]) 
        for unique_code in coupons.values('promo_code', 'expires_at', 'status').distinct():

            if unique_code['expires_at'] is not None and unique_code['expires_at'] <= now:
                status = "expired"

            else:
                if retailer.title == 'WorldMarket':
                    json_resp = requests.get('https://www.worldmarket.com/wmBasket.do?method=validateSourceCode&sourceCode=' + unique_code['promo_code'], headers={
                        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"
                        })
                    resp_dict = json_resp.json()
                    if not resp_dict["errMessage"]:
                        status = "valid"
                    else:
                        status = "invalid"

            coupons.filter(promo_code=unique_code['promo_code'], expires_at=unique_code['expires_at']).update(status=status, last_verified_date=now)
