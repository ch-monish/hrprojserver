from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response  
from rest_framework import status  
from .models import Industry
from .serializers import IndustrySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
import logging

logger = logging.getLogger(__name__)
class IndustryApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None): 
        industries = Industry.objects.all().order_by('IndustryName')
        industry_serializer = IndustrySerializer(industries, many=True)
        # logger.info(industry_serializer.data)
        return Response(industry_serializer.data)
    
    def post(self, request, format=None):
        industry_serializer = IndustrySerializer(data=request.data)
        if industry_serializer.is_valid():
            industry_serializer.save()
            logger.info(Messages1.ADD_SCFL)
            return Response(Messages1.ADD_SCFL)
        logger.error(industry_serializer.errors)
        return Response(industry_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        industries =  Industry.objects.get(IndustryId=request.data['IndustryId'])
        industry_serializer = IndustrySerializer(industries, data=request.data)
        if industry_serializer.is_valid():
            industry_serializer.save()
            logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL)
        logger.error(industry_serializer.errors)
        return Response(industry_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):      
        designations =  Industry.objects.get(IndustryId=pk)    
        designations.delete()
        logger.info(Messages1.DEL_SCFL)
        return Response(Messages1.DEL_SCFL)
       
