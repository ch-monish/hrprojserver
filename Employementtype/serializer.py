from rest_framework import serializers
from Employementtype.models import EmployementType
class EmployementSerializer(serializers.ModelSerializer):

    class Meta:
        model=EmployementType
        fields="__all__"