from rest_framework.serializers import ModelSerializer
from operationalmails.models import Operationalmails

class operationalMailsSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Operationalmails