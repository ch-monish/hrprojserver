from asyncio.windows_events import NULL
from dataclasses import fields
import json
from pyexpat import model
from rest_framework import serializers
from .models import BusinessUnit
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from django.contrib.auth.models import User

class  BusinessUnitSerializer(serializers.ModelSerializer):
    hrname = serializers.SerializerMethodField()

    def get_hrname(self, businessunit):
        user = User.objects.filter(username= businessunit.HR).first()
        if user is not None:
            return user.last_name+", "+user.first_name
        return None
    class Meta:
        model = BusinessUnit
        fields = '__all__'
    

    def validate_BusinessUnitName(self, value):
        # I assumed that you will that the string value, is a JSON object.
        # entered_name = json.loads(value).get('en', None)
        print(value)
        if value is None:
            raise serializers.ValidationError(Messages1.BN_Empty)
        #elif (value and Company.objects.filter(BusinessUnit Name=value).exists()):
          #  raise serializers.ValidationError("BusinessUnit name already exists!")
        # You need to return the value in after validation.
        return value   
   