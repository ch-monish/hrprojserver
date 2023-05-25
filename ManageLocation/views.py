from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response  
from rest_framework import status  
from .models import Location
from .serializers import LocationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
import logging

logger = logging.getLogger(__name__)

class LocationApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None): 
        locations = Location.objects.all()
        location_serializer = LocationSerializer(locations, many=True)
        # logger.info(location_serializer.data)
        return Response(location_serializer.data)
    
    def post(self, request, format=None):
        # location_data = JSONParser().parse(request)
        location_serializer = LocationSerializer(data=request.data)
        if location_serializer.is_valid():
            location_serializer.save()
            # return Response({"status": "success", "data": location_serializer.data}, status=status.HTTP_200_OK)  
            logger.info(Messages1.ADD_SCFL)
            return Response(Messages1.ADD_SCFL)
        logger.error(location_serializer.errors)
        return Response(location_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
        # else:
            # return Response({"status": "error", "data": company_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
    
    def put(self, request, format=None):
        # company_data = JSONParser().parse(request)
        locations =  Location.objects.get(LocationId=request.data['LocationId'])
        location_serializer = LocationSerializer(locations, data=request.data)
        if location_serializer.is_valid():
            location_serializer.save()
            logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL)
        logger.error(location_serializer.errors)
        return Response(location_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
       # return JsonResponse("Failed To update", safe=False)
    
    def delete(self, request, pk, format=None):      
        locations =  Location.objects.get(LocationId=pk)    
        locations.delete()
        logger.info(Messages1.DEL_SCFL)
        return Response(Messages1.DEL_SCFL)
       