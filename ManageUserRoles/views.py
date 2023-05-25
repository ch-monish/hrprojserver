from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .serializers import UserSerializer, PostUserSerializer
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
import logging
# Create your views here.

logger = logging.getLogger(__name__)
class UserRolesApi(APIView):

    def get(self, request, format=None):
        userroles = User.objects.all()
        user_serializer = UserSerializer(userroles, many=True)
        # logger.info(user_serializer.data)
        return Response(user_serializer.data)

    def post(self, request, format = None):
        # user_serializer = PostUserSerializer(data=request.data)
        users = User.objects.create_user(request.data['username'], request.data['email'], request.data['username'])
        users.first_name = request.data['first_name']
        users.last_name = request.data['last_name']
        users.is_active = request.data['is_active']
        # if user_serializer.is_valid():
            # user_serializer.save()
        users.save()
        # if user is not None: 
        groups = request.data['groups']
        for i in groups:
                g = Group.objects.get(id = i)
                g.user_set.add(users)
                logger.info(Messages1.ADD_SCFL)
        return Response(Messages1.ADD_SCFL)

    def put(self, request, format=None):
        userroles =  User.objects.get(id=request.data['id'])
        # userroles.last_name=request.data["last_name"]       
        # userroles.save()
        user_serializer = UserSerializer(userroles ,data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            groups = request.data['groups']
            for i in groups:
                g = Group.objects.get(id = i)
                g.user_set.add(userroles)
                logger.info(Messages1.UPD_SCFL)
            return Response(Messages1.UPD_SCFL)
        else:
            logger.error("Error")
            return Response("Error")

    def delete(self, request, pk, format=None):      
        userroles =  User.objects.get(id=pk)    
        userroles.delete()
        logger.info(Messages1.DEL_SCFL)
        return Response(Messages1.DEL_SCFL)

