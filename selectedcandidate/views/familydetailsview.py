import traceback
from candidate.models.selected_Candidates_Model import Selected_Candidates
from rest_framework.response import Response
from rest_framework import status
from candidate.models.selected_Candidates_Model import  Selected_Candidates
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from selectedcandidate.models.Candidatefamilydetails import CandidateFamilyDetails
from selectedcandidate.Serializers import candidatefamilydetailgetSerializer
from selectedcandidate.models import *
from candidate.models.selected_Candidates_Model import Selected_Candidates
import logging

logger = logging.getLogger(__name__)
class familydetailsview(ModelViewSet):
    @action(detail=True,methods=["post"])
    def createfamilydetail(self,request,format=None):
        try:
            # CandidatePersonalInfo.objects.all()
            CandidateFamilyDetails.objects.create(
            selectedCandidateId=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
    FullName=request.data["FullName"],
    Date_Of_Birth=request.data["Date_Of_Birth"],
    Relationship_with_employee=request.data["Relationship_with_employee"],
    Contact_Number=request.data["Contact_Number"],
            )
            logger.info("family detail created")
            return  Response("family detail created",status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            logger.error(e)
            logger.error(traceback.format_exc())
            return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=["post"])
    def updatefamilydetails(self,request,format=None):
        try:

            CandidateFamilyDetails.objects.filter(id=request.data["id"]).update(
                selectedCandidateId=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
    FullName=request.data["FullName"],
    Date_Of_Birth=request.data["Date_Of_Birth"],
    Relationship_with_employee=request.data["Relationship_with_employee"],
    Contact_Number=request.data["Contact_Number"],
            )
            logger.info("Family details updated succesfully")
            return Response("Family details updated succesfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=["post"])
    def getfamilydetails(self,request,format=None):
        try:

            fdo=CandidateFamilyDetails.objects.filter(selectedCandidateId_id=request.data["selectedcandidateid"])
            fdos=candidatefamilydetailgetSerializer(fdo,many=True).data
            # logger.info(fdos)
            return Response(fdos,status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    def deletefamilydetail(self,request,format=None):
        try:

            fdo=CandidateFamilyDetails.objects.filter(id=request.data["id"]).first()
            fdo.delete()
            logger.info("deleted Sucessfully")
            return Response("deleted Sucessfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)