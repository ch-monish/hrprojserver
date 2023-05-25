from django.shortcuts import render
from rest_framework.views import APIView
from Qualification.models import Qualification
from django.http.response import JsonResponse
from Qualification.serializer import QualifiacationSerializer
import logging
# Create your views here.
logger = logging.getLogger(__name__)
class QualificationDetails(APIView):
    def get(self,request,format=None):
        qualificationdetails=Qualification.objects.all()
        qualificationserializer=QualifiacationSerializer(qualificationdetails,many=True)
        # logger.info(qualificationserializer.data)
        return JsonResponse(qualificationserializer.data,safe=False)