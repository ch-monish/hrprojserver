"""HRproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# swagger
from rest_framework import permissions,authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



schema_view = get_schema_view(
    openapi.Info(
        title="HRPROJECT API",
        default_version='v1',
        description="Hr workflow",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
   
)

urlpatterns = [
    path('HRWorkflowServer/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('HRWorkflowServer/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
    path('HRWorkflowServer/api/company', include('managecompany.urls')),
    path('HRWorkflowServer/api/businessunit', include('managebusinessunit.urls')),
    path('HRWorkflowServer/api/serviceline', include('manageserviceline.urls')),
    path('HRWorkflowServer/api/Customer', include('ManageCustomer.urls')),
    path('HRWorkflowServer/api/Location', include('ManageLocation.urls')),
    path('HRWorkflowServer/api/Experience', include('ManageExperienceLevel.urls')),
    path('HRWorkflowServer/api/Designation', include('ManageDesignation.urls')),
    path('HRWorkflowServer/api/Band', include('ManageBand.urls')),
    path('HRWorkflowServer/api/SubBand', include('ManageSubBand.urls')),
    path('HRWorkflowServer/api/AvgCTC', include('ManageAvgCTC.urls')),
    path('HRWorkflowServer/api/Insurance', include('ManageInsurance.urls')),
    path('HRWorkflowServer/api/Roles', include('manageroles.urls')),
    path('HRWorkflowServer/api/UserRoles', include('ManageUserRoles.urls')),
    path('HRWorkflowServer/api/Industry', include('ManageIndustry.urls')),
    path('HRWorkflowServer/api/AdUsers', include('ManageAdUsers.urls')),
    path('HRWorkflowServer/api/stage', include('managestages.urls')),
    path('HRWorkflowServer/api/login', include('login.urls')),

    path('HRWorkflowServer/api/jobpost', include('jobpost.urls')),
    path('HRWorkflowServer/api/candidate', include('candidate.urls')),
    path('HRWorkflowServer/api/pdf', include('pdf.urls')),
    #  path('HRWorkflowServer/api/candidateFeedback', include('CandidateFeedback.urls')),
    path('HRWorkflowServer/api/Employementtype', include('Employementtype.urls')),
    path('HRWorkflowServer/api/Qualification', include('Qualification.urls')),

    path('HRWorkflowServer/api/Docx', include('document.urls')),
    path('HRWorkflowServer/api/selectedcandidate', include('selectedcandidate.urls')),
    path('HRWorkflowServer/api/zip', include('zipfiles.urls')),
    #  path('HRWorkflowServer/api/bank', include('bankdetails.urls')),
    path('HRWorkflowServer/api/info', include('DepartmentInfo.urls')),
    path('HRWorkflowServer/api/operationalmails', include('operationalmails.urls')),



    # swagger urls
    path('swagger1(?P<format>\.json|\.yaml)', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),

    path('swagger', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),


]
