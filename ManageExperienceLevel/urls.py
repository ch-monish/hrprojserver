from django.urls import path

from .views import ExperienceApi

urlpatterns=[
     path('', ExperienceApi.as_view()),
     path('/<int:pk>', ExperienceApi.as_view())
]