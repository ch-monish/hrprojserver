from django.urls import path
from .views import IndustryApi

urlpatterns=[
     path('', IndustryApi.as_view()),
     # path('/<int:pk>', IndustryApi.as_view())
]
