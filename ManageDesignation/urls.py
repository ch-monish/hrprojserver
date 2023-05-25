from django.urls import path
from .views import DesignationApi

urlpatterns=[
     path('', DesignationApi.as_view()),
     path('/<int:pk>', DesignationApi.as_view())
]