
# from managecompany.views import views
from django.urls import path

from managestages.views import StageApi


urlpatterns=[
     path('', StageApi.as_view()),
     # path('/<int:id>', views.companyApi)
]