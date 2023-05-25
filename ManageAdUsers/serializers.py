from asyncio.windows_events import NULL
from dataclasses import fields
import json
from pyexpat import model
from rest_framework import serializers
from ManageAdUsers.models import AdUsers
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1

class AdUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdUsers
        fields = '__all__'
    
    def validate_UserName(self, value):
        print(value)
        if value is None:
            raise serializers.ValidationError(Messages1.User_name_empty)
        return value 
    
    def validate_FirstName(self, value):
        print(value)
        if value is None:
            raise serializers.ValidationError(Messages1.FN_Empty)
        return value 

    def validate_LastName(self, value):
        print(value)
        if value is None:
            raise serializers.ValidationError(Messages1.LN_Empty)
        return value 

    def validate_Email(self, value):
        print(value)
        if value is None:
            raise serializers.ValidationError(Messages1.Email_Empty)
        return value   