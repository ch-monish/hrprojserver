from rest_framework import serializers
from .models import DepartmentInformation
from .models import BGVVendors

class  DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentInformation
        fields = '__all__'
class BGVVendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=BGVVendors
        fields='__all__'