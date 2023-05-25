import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.http.response import JsonResponse
from manageroles.serializers import GroupSerializer
import logging
# Create your views here.
logger = logging.getLogger(__name__)
class RolesApi(APIView):    
    
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None): 
        logger = logging.getLogger(__name__)
        roles = Group.objects.all()
        group_serializer = GroupSerializer(roles, many=True)
        # logger.info(group_serializer.data)
        return JsonResponse(group_serializer.data, safe=False)

    def post(self, request, format=None):
        group_serializer = GroupSerializer(data=request.data)
        if group_serializer.is_valid():
            group_serializer.save()
            # logger.info(group_serializer.data)
            return JsonResponse(group_serializer.data, safe=False)
        logger.error(group_serializer.errors)
        return JsonResponse(group_serializer.errors, safe=False)


