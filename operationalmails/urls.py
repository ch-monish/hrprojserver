from django.urls import path
from operationalmails.views import Operationalmailsview
# from .views import IndustryApi

urlpatterns=[
    #  path('', IndustryApi.as_view()),
    path("/getoperationalmails",Operationalmailsview.as_view({'post':"getoperationalmails"})),
    path("/sendoperationalmail",Operationalmailsview.as_view({'post':"sendoperationalmail"}))
    #  path('/<int:pk>', IndustryApi.as_view())
]
