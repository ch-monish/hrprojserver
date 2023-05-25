
import traceback
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from candidate.models.selected_Candidates_Model import Selected_Candidates
from candidate.models.candidatemodel import Candidate
from candidate.serializers import selectedcandidatesfulltimegridviewSerializer
from candidate.serializers import selectedcandidatescontractgridviewSerializer
from candidate.serializers import selectedcandidatesinterngridviewSerializer
from rest_framework import status
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)
class Selectedcandidatesgrids(ModelViewSet):
  @action(detail=True,methods=["get"])
  def getfulltimeselectedcandidates(self,request,format=None):
    try:
      # selcanob=Selected_Candidates.objects.filter(Candidate.EmploymentType="Full-Time")
      selcanob=Selected_Candidates.objects.filter(candidate__EmploymentType="Full-Time",VerificationStatus="verified").order_by("Created_on").reverse()
      serializer=selectedcandidatesfulltimegridviewSerializer(selcanob,many=True)
      # logger.info(serializer.data)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e: 
      logger.error(e)
      logger.error(traceback.format_exc())
      return Response(e, status=status.HTTP_400_BAD_REQUEST)
 
  @action(methods="get",detail=True)
  def getcontractselectedcandidates(self,request,format=None):
    try:
      # selcanob=Selected_Candidates.objects.filter(candidate__EmploymentType__in=["Contract(vendor)","Contract(direct)"])
      selcanob=Selected_Candidates.objects.filter(candidate__EmploymentType__in=["Contract(direct)"],VerificationStatus="verified").order_by("Created_on").reverse()
      serializer=selectedcandidatescontractgridviewSerializer(selcanob,many=True)
      # logger.info(serializer.data)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e: 
      logger.error(e)
      logger.error(traceback.format_exc())
      return Response(e, status=status.HTTP_400_BAD_REQUEST)
  
  @action(methods="get",detail=True)
  def getinternselectedcandidates(self,request,format=None):
    try:
      selcanob=Selected_Candidates.objects.filter(candidate__EmploymentType="Internship",VerificationStatus="verified").order_by("Created_on").reverse()
      serializer=selectedcandidatesinterngridviewSerializer(selcanob,many=True)
      # logger.info(serializer.data)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      logger.error(e) 
      logger.error(traceback.format_exc())
      return Response(e, status=status.HTTP_400_BAD_REQUEST)

    
