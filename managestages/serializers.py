from dataclasses import fields
from rest_framework import serializers

from managestages.models import Stage


class SatgeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Stage
        fields = '__all__'
 
