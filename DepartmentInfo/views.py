from django.shortcuts import render
from .models import DepartmentInformation
from .models import BGVVendors
from django.http.response import JsonResponse
from rest_framework.response import Response  
from rest_framework import status  
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from rest_framework.decorators import APIView
from .serializers import DepartmentSerializer
from .serializers import BGVVendorsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
import logging

# Create your views here.
logger = logging.getLogger(__name__)

class departmentApi(APIView):
    serializer_class = DepartmentSerializer
    def get(self, request, format=None): 
        info = DepartmentInformation.objects.all()
        info_serializer = DepartmentSerializer(info, many=True)
        logger.info(info_serializer.data)
        return JsonResponse(info_serializer.data, safe=False)
    
    def post(self, request, format=None):
        info_serializer = DepartmentSerializer(data=request.data)
        if info_serializer.is_valid():
            info_serializer.save()
            logger.info(Messages1.ADD_SCFL)
            return Response(Messages1.ADD_SCFL)
        logger.info(info_serializer.errors)
        return Response(info_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
       
    
    def put(self, request, format=None):
        info =  DepartmentInformation.objects.get(Id=request.data['Id'])
        info_serializer = DepartmentSerializer(info, data=request.data)
        if info_serializer.is_valid():
            info_serializer.save()
            logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL)
        logger.info(info_serializer.errors)
        return Response(info_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):      
        info =  DepartmentInformation.objects.get(Id=pk)    
        info.delete()
        logger.info(Messages1.DEL_SCFL)
        return Response(Messages1.DEL_SCFL)
       

class bgvvendorsview(ModelViewSet):
    @action(methods=['get'],detail=True)
    def getbgvvendors(self,format=None):
        try:
            bgvobj=BGVVendors.objects.filter()
            bgvserialied =BGVVendorsSerializer(bgvobj,many=True)
            # logger.info(bgvserialied.data)
            return Response(bgvserialied.data,status=status.HTTP_200_OK)
        except Exception  as e:
            logger.error("error : "+e)
            return Response("error : "+e,status=status.HTTP_400_BAD_REQUEST)
