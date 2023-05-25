from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from candidate.models.Candidate_Feedback_Model import Candidate_Feedback
from candidate.serializers import CandidateFeedBacksSerializer
import logging

logger = logging.getLogger(__name__)
class CandidateFeedBacks(APIView):
    def post(self,request,format=None):
        try:
            feedbacks = Candidate_Feedback.objects.filter(Candidate=request.data["Candidate_ID"])
            res = CandidateFeedBacksSerializer(feedbacks,many=True)
            # logger.info(res.data)
            return Response(res.data)    
        except:
            logger.error("Failed")
            return Response("Failed",status=status.HTTP_400_BAD_REQUEST)
            #prefetch related join tables a and b?