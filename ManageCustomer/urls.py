from django.urls import path
from ManageCustomer.views import CustomerApi

urlpatterns=[
     path('', CustomerApi.as_view()),
     path('/<int:pk>', CustomerApi.as_view())
]