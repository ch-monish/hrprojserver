
# from managecompany.views import views
from django.urls import path
from managecompany.views import companyApi

urlpatterns=[
     path('', companyApi.as_view()),
     path('/<int:pk>', companyApi.as_view())
]