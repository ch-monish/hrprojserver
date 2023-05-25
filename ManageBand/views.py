from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response  
from rest_framework import status  
from .models import Band
from .serializers import BandSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
import logging

logger = logging.getLogger(__name__)
class BandApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None): 
        bands = Band.objects.all()
        band_serializer = BandSerializer(bands, many=True)
        # logger.info(band_serializer.data)
        return JsonResponse(band_serializer.data, safe=False)
    
    def post(self, request, format=None):
        # band_data = JSONParser().parse(request)
        band_serializer = BandSerializer(data=request.data)
        if band_serializer.is_valid():
            band_serializer.save()
            # return Response({"status": "success", "data": band_serializer.data}, status=status.HTTP_200_OK)  
            logger.info(Messages1.ADD_SCFL)
            return Response(Messages1.ADD_SCFL)
        logger.error(band_serializer.errors)
        return Response(band_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
        # else:
            # return Response({"status": "error", "data": band_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
    
    def put(self, request, format=None):
        # band_data = JSONParser().parse(request)
        bands =  Band.objects.get(BandId=request.data['BandId'])
        band_serializer = BandSerializer(bands ,data=request.data)
        if band_serializer.is_valid():
            band_serializer.save()
            logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL)
        logger.error(band_serializer.errors)
        return Response(band_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
       # return JsonResponse("Failed To update", safe=False)
    
    def delete(self, request, pk, format=None):      
        bands =  Band.objects.get(BandId=pk)    
        bands.delete()
        logger.info(Messages1.DEL_SCFL)
        return Response(Messages1.DEL_SCFL)
       