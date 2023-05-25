from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response  
from rest_framework import status  
from .models import Designation
from .serializers import DesignationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
import logging

logger = logging.getLogger(__name__)
class DesignationApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None): 
        designations = Designation.objects.all().order_by('DesignationName')
        designation_serializer = DesignationSerializer(designations, many=True)
        # logger.info(designation_serializer.data)
        return JsonResponse(designation_serializer.data, safe=False)
    
    def post(self, request, format=None):
        # designation_data = JSONParser().parse(request)
        designation_serializer = DesignationSerializer(data=request.data)
        if designation_serializer.is_valid():
            designation_serializer.save()
            # return Response({"status": "success", "data": designation_serializer.data}, status=status.HTTP_200_OK)  
            logger.info(Messages1.ADD_SCFL)
            return Response(Messages1.ADD_SCFL)
        logger.error(designation_serializer.errors)
        return Response(designation_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
        # else:
            # return Response({"status": "error", "data": designation_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
    
    def put(self, request, format=None):
        # designation_data = JSONParser().parse(request)
        designations =  Designation.objects.get(DesignationId=request.data['DesignationId'])
        designation_serializer = DesignationSerializer(designations, data=request.data)
        if designation_serializer.is_valid():
            designation_serializer.save()
            logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL)
        logger.error(designation_serializer.errors)
        return Response(designation_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
       # return JsonResponse("Failed To update", safe=False)
    
    def delete(self, request, pk, format=None):      
        designations =  Designation.objects.get(DesignationId=pk)    
        designations.delete()
        logger.info(Messages1.DEL_SCFL)
        return Response(Messages1.DEL_SCFL)
       
