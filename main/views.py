from uuid import uuid4
from urllib.parse import urlparse
from django.http import JsonResponse
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from scrapyd_api import ScrapydAPI
from .models import CouponItem, Retailer, CouponSite, CrawlTask
from .serializers import CouponItemSerializer

import time

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True


class CouponItemView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouponItemSerializer

    def get(self, request):
        # retailers = request.data.get('retailers', [])
        retailers = Retailer.objects.all()
        # coupons = CouponItem.objects.filter(retailer_slug_id__in=retailers)
        coupons = CouponItem.objects.all()
        serializer = self.serializer_class(coupons, many=True)

        response = {}
        for retailer in retailers:
            response[retailer.slug_id] = []
        for data in serializer.data:
            errors = data.get('errors', None)
            retailer_id = data.get('retailer', None)
            retailer = Retailer.objects.get(pk=retailer_id)

            if errors is not None:
                return super(UserJSONRenderer, self).render(data)

            if retailer is not None:
                data['retailer'] = retailer.title
            response[retailer.slug_id].append(data)

        return Response(response)


def start_crawling(self):
    print("=====================crawling started==================")
    time.sleep(1)

    retailers = Retailer.objects.all()
    for retailer in retailers:
        coupon_sites = retailer.coupon_sites.all()
        for coupon_site in coupon_sites:
            url = coupon_site.link
            domain = urlparse(url).netloc  # parse the url and extract the domain
            unique_id = str(uuid4())  # create a unique ID.
            retailer_title = retailer.title
            page_link = coupon_site.page_link

            # This is the custom settings for scrapy spider.
            # We can send anything we want to use it inside spiders and pipelines.
            # I mean, anything
            settings = {
                'unique_id': unique_id,  # unique ID for each record for DB
            }

            # Here we schedule a new crawling task from scrapyd.
            # Notice that settings is a special argument name.
            # But we can pass other arguments, though.
            # This returns a ID which belongs and will be belong to this task

            task = scrapyd.schedule('default', 'coucrawler',
                                    settings=settings, url=url, domain=domain, retailer=retailer_title,
                                    page_link=page_link)


def check_task_status():
    tasks = CrawlTask.objects.all()
    for task in tasks:
        if not task.status is "FINISHED":
            now = timezone.now()
            status = scrapyd.job_status('default', task.task_id)
            if status == 'pending':
                task.status = 'PENDING'
            if status == 'running':
                task.status = 'RUNNING'
            if status == 'finished':
                task.status = 'finished'
            task.save()
