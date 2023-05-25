from django.urls import path
from .views import  zipallfiles

urlpatterns=[
     path('', zipallfiles.as_view({'post': 'create_zip'}))
     # path('/<int:pk>', create_zip.as_view())
]