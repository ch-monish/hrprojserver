from django.urls import path
from .views import InsuranceApi

urlpatterns=[
     path('', InsuranceApi.as_view()),
     path('/<int:pk>', InsuranceApi.as_view())
]