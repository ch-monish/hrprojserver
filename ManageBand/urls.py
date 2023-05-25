from django.urls import path
from .views import BandApi

urlpatterns=[
     path('', BandApi.as_view()),
     path('/<int:pk>', BandApi.as_view())
]