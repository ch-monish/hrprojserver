from django.urls import path
from .views import ServiceLineApi

urlpatterns=[
     path('', ServiceLineApi.as_view()),
     path('/<int:pk>', ServiceLineApi.as_view())
]