from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response  
from rest_framework import status  
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
import logging

logger = logging.getLogger(__name__)
class CustomerApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None): 
        customers = Customer.objects.all()
        customer_serializer = CustomerSerializer(customers, many=True)
        # logger.info(customer_serializer.data)
        return JsonResponse(customer_serializer.data, safe=False)
    
    def post(self, request, format=None):
        # customer_data = JSONParser().parse(request)
        customer_serializer = CustomerSerializer(data=request.data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            # return Response({"status": "success", "data": customer_serializer.data}, status=status.HTTP_200_OK)  
            logger.info(Messages1.ADD_SCFL)
            return Response(Messages1.ADD_SCFL)
        logger.error(customer_serializer.errors)
        return Response(customer_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
        # else:
            # return Response({"status": "error", "data": customer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
    
    def put(self, request, format=None):
        # customer_data = JSONParser().parse(request)
        customers =  Customer.objects.get(CustomerId=request.data['CustomerId'])
        customer_serializer = CustomerSerializer(customers, data=request.data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL) 
        logger.error(customer_serializer.errors)
        return Response(customer_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST)
        #return JsonResponse("Failed To update", safe=False)
    
    def delete(self, request, pk, format=None):      
        customers =  Customer.objects.get(CustomerId=pk)    
        customers.delete()
        logger.info(Messages1.DEL_SCFL)
        return Response(Messages1.DEL_SCFL)

