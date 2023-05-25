from django.urls import path
from . import views
  
urlpatterns = [
    path('hv/', views.HelloView.as_view(), name ='hello'),
]