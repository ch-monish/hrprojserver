from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from candidate.models.Feedback_Category_Model import Feedback_Category
from candidate.serializers import FeedbackFieldsSerializer
import logging

logger = logging.getLogger(__name__)
class FeedbackFields(APIView):
    def post(self,request,format=None):
        try:
            feedbackfields = Feedback_Category.objects.filter(Stage=request.data["stagename"])
            res = FeedbackFieldsSerializer(feedbackfields, many=True)
            # logger.info(res.data)
            return Response(res.data)    
        except:
            logger.error("Failed")
            return Response("failed",status=status.HTTP_400_BAD_REQUEST)
