# movie_collection/middleware.py
from django.db import transaction
from .models import RequestCount

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.increment_request_count()
        response = self.get_response(request)
        return response

    def increment_request_count(self):
        with transaction.atomic():
            obj, created = RequestCount.objects.select_for_update().get_or_create(id=1)
            obj.count += 1
            obj.save()
