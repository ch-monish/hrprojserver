from asyncio.windows_events import NULL
from dataclasses import fields
import json
from pyexpat import model
from rest_framework import serializers
from .models import Industry
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from django.contrib.auth.models import User

class IndustrySerializer(serializers.ModelSerializer):
    industryheadname = serializers.SerializerMethodField()

    def get_industryheadname(self, industry):
        user = User.objects.filter(username= industry.IndustryHead).first()
        if user is not None:
            return user.last_name+", "+user.first_name
        return None
    class Meta:
        model = Industry
        fields = '__all__'
        extra_kwargs = {"content": {"trim_whitespace": True}}
    

    def validate_IndustryName(self, value):
        print(value)
        if value is None:
            raise serializers.ValidationError(Messages1.IN_Empty)
        return value   