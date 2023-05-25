from django.urls import path
from Employementtype.views import Employementdetails
urlpatterns=[

    path('',Employementdetails.as_view())
]