from django.views import View
from django.http  import JsonResponse

from events.models import ProductEvent, CategoryEvent, SloganEvent
from events.response import events_schema_dict

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class EventView(View):
    @swagger_auto_schema(manual_parameters = [], responses = events_schema_dict)
    def get(self, request):
        try:
            product_events_count  = int(request.GET.get('product-events-count', 4))
            category_events_count = int(request.GET.get('category-events-count', 2))

            product_events  = ProductEvent.objects.all().order_by('-created_at')[:product_events_count]
            category_events = CategoryEvent.objects.all().order_by('-created_at')[:category_events_count]
            slogan_event    = SloganEvent.objects.all().order_by('-created_at').first()

            product_events_results = [
                {
                    "image_url"       : product_event.image_url,
                    "product_name"    : product_event.product.name,
                    "product_summary" : product_event.product.summary,
                    "product_id"      : product_event.product.id
                } for product_event in product_events]

            category_events_results = [
                {
                    "image_url"   : category_event.image_url,
                    "category_id" : category_event.category_id,
                    "title"       : category_event.title,
                    "description" : category_event.description
                } for category_event in category_events]

            slogan_events_results = {
                    "image_url" : slogan_event.image_url,
                    "slogan"    : slogan_event.slogan
                } 
            
            results = {
                "product_events"  : product_events_results,
                "category_events" : category_events_results,
                "slogan_events"   : slogan_events_results
            }

            return JsonResponse({"results": results}, status=200)
        
        except ValueError:
            return JsonResponse({"message": "INVALID_COUNT"}, status=400)
