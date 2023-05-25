from django.urls import path
from .views import BusinessUnitApi

urlpatterns=[
     path('', BusinessUnitApi.as_view()),
     path('/<int:pk>', BusinessUnitApi.as_view())
]