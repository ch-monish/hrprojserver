from django.urls import path
from .views import LocationApi

urlpatterns=[
     path('', LocationApi.as_view()),
     path('/<int:pk>', LocationApi.as_view())
]