from django.urls import path
from .views import departmentApi
from .views import bgvvendorsview

urlpatterns=[
     path('', departmentApi.as_view()),
     path('/bgvvendors', bgvvendorsview.as_view({"get":'getbgvvendors'})),

]