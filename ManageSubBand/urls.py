from django.urls import path
from .views import SubBandApi

urlpatterns=[
     path('', SubBandApi.as_view()),
     path('/<int:pk>', SubBandApi.as_view())
]