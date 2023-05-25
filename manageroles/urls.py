
# from managecompany.views import views
from django.urls import path

from manageroles.views import RolesApi

urlpatterns=[
     path('', RolesApi.as_view()),
     # path('/<int:id>', views.companyApi)
]