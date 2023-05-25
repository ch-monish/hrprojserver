import traceback
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from candidate.models.selected_Candidates_Model import Selected_Candidates
from candidate.serializers import selectedcandidatesgridviewSerializer
# from selectedcandidate.models.CandidatePersonalInfo import *
import logging

logger = logging.getLogger(__name__)
class SelectedCandidateAction(ModelViewSet):
    @action(detail=True, methods=['post'])
    def selectedcandidatedetailsbyusername(self, request, format=None):
        try:
            # CandidatePersonalInfo.objects.all()
            print(request.data)
            selectedcandidate = Selected_Candidates.objects.filter(
                username=request.data["username"]).first()
            selectedcandidateserializer = selectedcandidatesgridviewSerializer(
                selectedcandidate)
            # logger.info(selectedcandidateserializer.data)
            return Response(selectedcandidateserializer.data)
        except Exception as ex:
            logger.error(str(ex)+"error while fetching selcted candidate data")
            logger.error(traceback.format_exc())
            return Response(str(ex)+"error while fetching selcted candidate data",status=status.HTTP_400_BAD_REQUEST)