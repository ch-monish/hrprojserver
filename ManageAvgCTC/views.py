from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response  
from rest_framework import status  
from .models import AvgCTC
from .serializers import AvgCTCSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
import logging

logger = logging.getLogger(__name__)
class AvgCTCApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None): 
        avgCTC = AvgCTC.objects.all()
        avgCTC_serializer = AvgCTCSerializer(avgCTC, many=True)
        # logger.info(avgCTC_serializer.data)
        return JsonResponse(avgCTC_serializer.data, safe=False)
    
    def post(self, request, format=None):
        # avgCTC_data = JSONParser().parse(request)
        avgCTC_serializer = AvgCTCSerializer(data=request.data)
        if avgCTC_serializer.is_valid():
            avgCTC_serializer.save()
            # return Response({"status": "success", "data": avgCTC_serializer.data}, status=status.HTTP_200_OK)  
            logger.info(Messages1.ADD_SCFL)
            return Response(Messages1.ADD_SCFL)
        logger.error(avgCTC_serializer.errors)
        return Response(avgCTC_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
        # else:
            # return Response({"status": "error", "data": avgCTC_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
    
    def put(self, request, format=None):
        # avgCTC_data = JSONParser().parse(request)
        avgCTC =  AvgCTC.objects.get(Id=request.data['Id'])
        avgCTC_serializer = AvgCTCSerializer(avgCTC ,data=request.data)
        if avgCTC_serializer.is_valid():
            avgCTC_serializer.save()
            logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL)
        logger.error(avgCTC_serializer.errors)
        return Response(avgCTC_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
       # return JsonResponse("Failed To update", safe=False)
    
    def delete(self, request, pk, format=None):      
        avgCTC =  AvgCTC.objects.get(Id=pk)    
        avgCTC.delete()
        logger.info(Messages1.DEL_SCFL)
        return Response(Messages1.DEL_SCFL)