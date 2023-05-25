import traceback
from rest_framework.response import Response
from rest_framework import status
from candidate.models.selected_Candidates_Model import  Selected_Candidates
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from selectedcandidate.models.Candidateinsurancedetails import CandidateInsuranceDetails
from selectedcandidate.Serializers import candidateinsurancedetailgetSerializer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
class insurancedetailsview(ModelViewSet):
    @action(detail=True,methods=["post"])
    def createinsurancedetail(self,request,format=None):
        try:
            # CandidatePersonalInfo.objects.all()
            CandidateInsuranceDetails.objects.create(
            Selected_Candidate_ID=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
            Name=request.data["Name"],
            DateOfBirth=request.data["DateOfBirth"],
            Relationship=request.data["Relationship"],
            Gender=request.data["Gender"],
            Age=datetime.now().year-datetime.strptime(request.data["DateOfBirth"],"%Y-%M-%d").year
            # PercentageofInsurance=request.data["PercentageofInsurance"],
            )
            logger.info("Insurance detail created")
            return Response("Insurance detail created",status=status.HTTP_200_OK)
        
        except Exception as e: 
            # print(e)
            logger.error(e)
            logger.error(traceback.format_exc())
            return Response(e,status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=["post"])
    def updateinsurancedetail(self,request,format=None):
        try:

            CandidateInsuranceDetails.objects.filter(Id=request.data["Id"]).update(
                Selected_Candidate_ID=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
                Name=request.data["Name"],
                DateOfBirth=request.data["DateOfBirth"],
                Relationship=request.data["Relationship"],
                Gender=request.data["Gender"],
                Age=datetime.now().year-datetime.strptime(request.data["DateOfBirth"],"%Y-%M-%d").year
                # PercentageofInsurance=request.data["PercentageofInsurance"],
            
            )
            logger.info("Insurance details updated succesfully")
            return Response("Insurance details updated succesfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=["post"])
    def getinsurancedetails(self,request,format=None):
        try:

            ido=CandidateInsuranceDetails.objects.filter(Selected_Candidate_ID_id=request.data["selectedcandidateid"])
            idos=candidateinsurancedetailgetSerializer(ido,many=True).data
            # logger.info(idos)
            return Response(idos,status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    def deleteinsurancedetail(self,request,format=None):
        try:

            ido=CandidateInsuranceDetails.objects.filter(Id=request.data["Id"]).first()
            ido.delete()
            logger.info("Deleted Sucessfully")
            return Response("Deleted Sucessfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
        
   