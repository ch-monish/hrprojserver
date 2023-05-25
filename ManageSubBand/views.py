from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response  
from rest_framework import status  
from .models import SubBand
from .serializers import SubBandSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
import logging

logger = logging.getLogger(__name__)

class SubBandApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None): 
        subbands = SubBand.objects.all()
        subband_serializer = SubBandSerializer(subbands, many=True)
        # logger.info(subband_serializer.data)
        return JsonResponse(subband_serializer.data, safe=False)
    
    def post(self, request, format=None):
        # subband_data = JSONParser().parse(request)
        subband_serializer = SubBandSerializer(data=request.data)
        if subband_serializer.is_valid():
            subband_serializer.save()
            # return Response({"status": "success", "data": subband_serializer.data}, status=status.HTTP_200_OK)  
            logger.error(Messages1.ADD_SCFL)
            return Response(Messages1.ADD_SCFL)
        # logger.info(subband_serializer.errors)
        return Response(subband_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
        # else:
            # return Response({"status": "error", "data": subband_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
    
    def put(self, request, format=None):
        # subband_data = JSONParser().parse(request)
        subbands =  SubBand.objects.get(SubBandId=request.data['SubBandId'])
        subband_serializer = SubBandSerializer(subbands, data=request.data)
        if subband_serializer.is_valid():
            subband_serializer.save()
            logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL)
        # logger.info(subband_serializer.errors)
        return Response(subband_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
       # return JsonResponse("Failed To update", safe=False)
    
    def delete(self, request, pk, format=None):      
        subbands =  SubBand.objects.get(SubBandId=pk)    
        subbands.delete()
        logger.info(Messages1.DEL_SCFL)
        return JsonResponse(Messages1.DEL_SCFL, safe=False)
       