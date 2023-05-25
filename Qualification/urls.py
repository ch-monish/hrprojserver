from django.urls import path
from Qualification.views import QualificationDetails
urlpatterns=[

    path('',QualificationDetails.as_view())
]