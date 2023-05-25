
# from managecompany.views import views
from django.urls import path

from login.views import LoginApi

urlpatterns=[
     path('', LoginApi.as_view()),
]