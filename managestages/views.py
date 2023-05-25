from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from managestages.models import Stage
from managestages.serializers import SatgeSerializer
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class StageApi(APIView):    
    
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None): 
        stages = Stage.objects.all()
        stage_serializer = SatgeSerializer(stages, many=True)
        # logger.info(stage_serializer.data)
        return JsonResponse(stage_serializer.data, safe=False)

    def post(self, request, format=None):
        stage_serializer = SatgeSerializer(data=request.data)
        if stage_serializer.is_valid():
            stage_serializer.save()
            # logger.info(stage_serializer.data)
            return JsonResponse(stage_serializer.data, safe=False)
        logger.error(stage_serializer.errors)
        return JsonResponse(stage_serializer.errors, safe=False)
