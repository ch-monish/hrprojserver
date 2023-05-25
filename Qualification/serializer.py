from rest_framework import serializers
from Qualification.models import Qualification
class QualifiacationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Qualification
        fields="__all__"