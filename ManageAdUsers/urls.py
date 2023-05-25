from django.urls import path
from .views import UsersApi

urlpatterns=[
     path('', UsersApi.as_view()),
     path('/<int:pk>', UsersApi.as_view())
]