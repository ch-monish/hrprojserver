from django.urls import path

from .views import AvgCTCApi

urlpatterns=[
     path('', AvgCTCApi.as_view()),
     path('/<int:pk>', AvgCTCApi.as_view())
]