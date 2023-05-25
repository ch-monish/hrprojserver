from django.urls import path
from .views import UserRolesApi

urlpatterns=[
     path('', UserRolesApi.as_view()),
     path('/<int:pk>', UserRolesApi.as_view())
]