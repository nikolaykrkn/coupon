from uuid import uuid4
from urllib.parse import urlparse
from django.http import JsonResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from scrapyd_api import ScrapydAPI
from main.models import CouponItem, Retailer, CouponSite
from .serializers import CouponItemSerializer

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


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

    def put(self, request):
        
        retailers = Retailer.objects.all()
        for retailer in retailers:
            if not is_valid_url(retailer.link):
                continue
        
        domain = urlparse(url).netloc # parse the url and extract the domain
        unique_id = str(uuid4()) # create a unique ID. 
        
        # This is the custom settings for scrapy spider. 
        # We can send anything we want to use it inside spiders and pipelines. 
        # I mean, anything
        settings = {
            'unique_id': unique_id, # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # Here we schedule a new crawling task from scrapyd. 
        # Notice that settings is a special argument name. 
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.
        task = scrapyd.schedule('default', 'icrawler', 
            settings=settings, url=url, domain=domain)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })

    Get requests are for getting result of a specific crawling task
    def get(self, request):
        retailers = request.data.get('retailers', [])
        # coupons = CouponItem.objects.filter(retailer_title__in=retailers)
        coupons = CouponItem.objects.all()
        serializer = self.serializer_class(coupons, many=True)
        return Response(serializer.data)

    #     # We were passed these from past request above. Remember ?
    #     # They were trying to survive in client side.
    #     # Now they are here again, thankfully. <3
    #     # We passed them back to here to check the status of crawling
    #     # And if crawling is completed, we respond back with a crawled data.
    #     # task_id = request.GET.get('task_id', None)
    #     # unique_id = request.GET.get('unique_id', None)

    #     # if not task_id or not unique_id:
    #     #     return JsonResponse({'error': 'Missing args'})

    #     # Here we check status of crawling that just started a few seconds ago.
    #     # If it is finished, we can query from database and get results
    #     # If it is not finished we can return active status
    #     # Possible results are -> pending, running, finished
    #     # status = scrapyd.job_status('default', task_id)
    #     # if status == 'finished':
    
    # def get(self, request, pk):
    #     coupon_list = CouponItem.objects.all() 
    #     data = PollSerializer(poll).data
    #     return Response(data)
    #     # Call the base implementation first to get the context
    #     context = super(CouponListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     try:
    #         # this is the unique_id that we created even before crawling started.
            
    #         context['coupons'] = coupons
    #     except Exception as e:
    #         context['coupons'] = str(e)
    #     return context
    
        