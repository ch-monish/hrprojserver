import logging
import this
import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
# from ms_active_directory import ADDomain
from rest_framework.response import Response
from rest_framework import status  

from login.serializers import LoginSerializer, UserSerializer
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from django.contrib.auth.models import User, Group
from   . import ldapfun
from Scheduler.Task1 import ManageADUsers
from rest_framework.permissions import AllowAny
import logging
from decouple import config
# Create your views here.

logger = logging.getLogger(__name__)
class LoginApi(APIView):
    permission_classes = (AllowAny,) 
    def post(self, request, format=None): 
        # loginSerializer = LoginSerializer(data=request.data)
        try:
            user = User.objects.filter(username= request.data['User_name'],is_active=True).first()
            # user = authenticate(username=request.data['User_name'], password =request.data['User_name'] )
            
            if user is not None:
                groupsdetails =user.groups.all()
                if groupsdetails.contains(Group.objects.filter(name = 'Candidate').first() ):
                    user = authenticate(username=request.data['User_name'], password =request.data['password'] )
                    if user is None:
                        logger.info(Messages1.UNF)
                        return Response(Messages1.UNF, status=status.HTTP_403_FORBIDDEN)          
                else:
                    if config("AD_AUTHENTICATION")=="True":
                    #    Active directory validation
                        print("executing ldap fun")
                        res=ldapfun.connecttoad(user.email,request.data['password'] )
                        if res==True:
                            print("")
                        else:
                            logger.info("Invalid Credentials")
                            return Response("Invalid Credentials", status=status.HTTP_403_FORBIDDEN)
                        # ManageADUsers()
                      
                userserializer =  UserSerializer(user)
                # userserializer.data
                # refresh = RefreshToken.for_user(user)
                # return Response({
                #     'refresh': str(refresh),
                #     'access': str(refresh.access_token),
                # })
                logger.info(userserializer.data)
                return Response(userserializer.data, status=status.HTTP_200_OK)
                # l = user.groups.values_list('name',flat = True) # QuerySet Object
                # l_as_list = list(l)   
                # print(l_as_list)
            else:
                logger.info(Messages1.INVC)
                return Response(Messages1.INVC, status=status.HTTP_403_FORBIDDEN)
        except Exception as ex:
                logger.error(Messages1.INVC)
                logger.error(traceback.format_exc())
                return Response(Messages1.INVC, status=status.HTTP_403_FORBIDDEN)


            

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }