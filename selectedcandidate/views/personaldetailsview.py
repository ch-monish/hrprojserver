import traceback
from candidate.models.selected_Candidates_Model import Selected_Candidates
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from candidate.models.candidatemodel import Candidate
from candidate.models.selected_Candidates_Model import  Selected_Candidates
from jobpost.models.jobpostapprovalmodel import JobPostApproval
from candidate.serializers import selectedcandidatesgridviewSerializer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from ManageBand.models import Band
from ManageSubBand.models import SubBand
from ManageDesignation.models import Designation
from datetime import datetime
from selectedcandidate.models.Candidatepersonalinfo import CandidatePersonalInfo
from selectedcandidate.Serializers import candidatepersonalinfogetSerializer
from selectedcandidate.models import *
from candidate.models.selected_Candidates_Model import Selected_Candidates
import logging

logger = logging.getLogger(__name__)
class personaldetialsview(ModelViewSet):
    @action(detail=True,methods=["post"])
    def createpersonaldetails(self,request,format=None):
        try:
            # CandidatePersonalInfo.objects.all()
            CandidatePersonalInfo.objects.create(
            selectedCandidateid=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedCandidateid"]).first(),
            Name=request.data["Name"],
            DateOfBirth=request.data["DateOfBirth"],
            Marital_status=request.data["Marital_status"],
            Gender=request.data["Gender"],
            BloodGroup=request.data["BloodGroup"],
            PAN=request.data["PAN"],
            AADHAR=request.data["AADHAR"],
            Email=request.data["Email"],
            ContactNumber=request.data["ContactNumber"],
            EmergencycontactName=request.data["EmergencycontactName"],
            EmergencycontactRelation=request.data["EmergencycontactRelation"],
            EmergencycontactNumber=request.data["EmergencycontactNumber"],
            PassportNumber=request.data["PassportNumber"],
            PassportValidFrom=request.data["PassportValidFrom"],
            PassportValidTo=request.data["PassportValidTo"],
            Address=request.data["Address"],
            )
            logger.info("personal info saved succesfully")
            return Response("personal info saved succesfully",status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            logger.error(e)
            logger.error(traceback.format_exc())
            return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=["post"])
    def updatepersonaldetails(self,request,format=None):
        try:

            CandidatePersonalInfo.objects.filter(selectedCandidateid_id=request.data["selectedCandidateid"]).update(
                 Name=request.data["Name"],
            DateOfBirth=request.data["DateOfBirth"],
            Marital_status=request.data["Marital_status"],
            Gender=request.data["Gender"],
            BloodGroup=request.data["BloodGroup"],
            PAN=request.data["PAN"],
            AADHAR=request.data["AADHAR"],
            Email=request.data["Email"],
            ContactNumber=request.data["ContactNumber"],
            EmergencycontactName=request.data["EmergencycontactName"],
            EmergencycontactRelation=request.data["EmergencycontactRelation"],
            EmergencycontactNumber=request.data["EmergencycontactNumber"],
            PassportNumber=request.data["PassportNumber"],
            PassportValidFrom=request.data["PassportValidFrom"],
            PassportValidTo=request.data["PassportValidTo"],
            Address=request.data["Address"],
            )
            logger.info("personal info updated Succesfully ")
            return Response("personal info updated Succesfully ",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=["post"])
    def getpersonaldetails(self,request,format=None):
        try:

            cpo=CandidatePersonalInfo.objects.filter(selectedCandidateid_id=request.data["selectedcandidateid"]).first()
            cpos=candidatepersonalinfogetSerializer(cpo,many=False).data
            logger.info(cpos)
            return Response(cpos,status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)