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

from .models import CouponItem, Retailer, CouponSite, CrawlTask
from .serializers import CouponItemSerializer

import time


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) # check if url format is valid
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
