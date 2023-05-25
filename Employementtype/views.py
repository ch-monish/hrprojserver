from django.shortcuts import render
from rest_framework.views import APIView
from .models import EmployementType
from django.http.response import JsonResponse
from Employementtype.serializer import EmployementSerializer
import logging
# Create your views here.
logger = logging.getLogger(__name__)

class Employementdetails(APIView):
    def get(self,request,format=None):
        employementdetails=EmployementType.objects.all()
        employeserializer=EmployementSerializer(employementdetails,many=True)
        # logger.info(employeserializer.data)
        return JsonResponse(employeserializer.data,safe=False)