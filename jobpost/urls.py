from django.urls import path

from jobpost.views.jobpostactions import JobPostAction
from jobpost.views.usersByGroup import usersByGroup
from .views.jobpostinsert import JobPostApi
from .views.myjobpostdetails import MyJobPostDetails

urlpatterns=[
     path('/addjobpost', JobPostApi.as_view()),
     path('/myjobposts', MyJobPostDetails.as_view({'post': 'getmyjobpostdetails'})),
     path('/jobpostcancel', MyJobPostDetails.as_view({'post': 'canceljobpost'})),
     path('/jobpostactionsdetails', JobPostAction.as_view({'post': 'jobpostactiondetails'})),
     path('/jobpostactionssubmit', JobPostAction.as_view({'post': 'jobpostactionsubmit'})),
     path('/usersbyrole', usersByGroup.as_view()),
     # path('/<int:pk>', BusinessUnitApi.as_view())
]