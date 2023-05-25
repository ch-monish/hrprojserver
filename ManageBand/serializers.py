from asyncio.windows_events import NULL
from dataclasses import fields
import json
from pyexpat import model
from rest_framework import serializers
from .models import Band
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1

class  BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = '__all__'
    

    def validate_BandName(self, value):
        # I assumed that you will that the string value, is a JSON object.
        # entered_name = json.loads(value).get('en', None)
        print(value)
        if value is None:
            raise serializers.ValidationError(Messages1.BN_Empty)
        #elif (value and Company.objects.filter(BandName=value).exists()):
          #  raise serializers.ValidationError("Band name already exists!")
        # You need to return the value in after validation.
        return value 
