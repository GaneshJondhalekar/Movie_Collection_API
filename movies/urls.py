
from django.urls import path

from .views import *

urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('movies/',MovieListView.as_view(),name='movies'),
    path('collection/',CollectionAPIView.as_view(),name='create_retieve_collection'),
    path('collection/<uuid:uuid>/', DetailCollectionAPIView.as_view(), name='collection_detail'),
    path('request-count/', RequestCountAPIView.as_view(), name='request-count'),
    path('request-count/reset/', ResetRequestCountAPIView.as_view(), name='reset-request-count'),
]