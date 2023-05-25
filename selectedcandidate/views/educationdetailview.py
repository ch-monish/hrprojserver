import traceback
from candidate.models.selected_Candidates_Model import Selected_Candidates
from rest_framework.response import Response
from rest_framework import status
from candidate.models.selected_Candidates_Model import  Selected_Candidates
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from selectedcandidate.models.Candidatedducationaldetails import CandidateEducationalDetails
from selectedcandidate.Serializers import candidateeducationdetailgetSerializer
from selectedcandidate.models import *
from candidate.models.selected_Candidates_Model import Selected_Candidates
from selectedcandidate.models.Documentsupload import CandidateDocumentsUpload
import logging
import os
from django.db import transaction
from HRproj.settings import MEDIA_ROOT, MEDIA_URL, BASE_DIR


logger = logging.getLogger(__name__)
class educationdetailsview(ModelViewSet):
    @action(detail=True,methods=["post"])
    def createeducationdetail(self,request,format=None):
        try:
            # CandidatePersonalInfo.objects.all()
            CandidateEducationalDetails.objects.create(
            selectedCandidateId=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
    Qualification=request.data["Qualification"],
    Specialization=request.data["Specialization"],
    Start_Date=request.data["Start_Date"],
    End_Date=request.data["End_Date"],
    Institute=request.data["Institute"],
    Percentage=request.data["Percentage"],
            )
            logger.info("education detail created")
            return  Response("education detail created",status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            logger.error(e)
            logger.error(traceback.format_exc())
            return  Response(e,status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True,methods=["post"])
    def updateeducationdetails(self,request,format=None):
        try:

            CandidateEducationalDetails.objects.filter(id=request.data["id"]).update(
                   selectedCandidateId=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
    Qualification=request.data["Qualification"],
    Specialization=request.data["Specialization"],
    Start_Date=request.data["Start_Date"],
    End_Date=request.data["End_Date"],
    Institute=request.data["Institute"],
    Percentage=request.data["Percentage"],
            )
            logger.info("education detail updated ")
            return  Response("education detail updated ",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return  Response(e,status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True,methods=["post"])
    def geteducationdetails(self,request,format=None):
        try:

            edo=CandidateEducationalDetails.objects.filter(selectedCandidateId_id=request.data["selectedcandidateid"])
            edos=candidateeducationdetailgetSerializer(edo,many=True).data
            # logger.info(edos)
            return  Response(edos,status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return  Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    def deleteeducationdetail(self,request,format=None):
        try:
            with transaction.atomic():
                edo=CandidateEducationalDetails.objects.filter(id=request.data["id"]).first()
                edo.delete()
                candidatedocob=CandidateDocumentsUpload.objects.filter(detailtype="Education",detailtypeId=request.data["id"])

                for i in candidatedocob:
                
                    filename =i.file
                    filename = os.path.join(MEDIA_ROOT, str(filename))
                    filename = filename.replace("/", "\\")
                    if os.path.exists(filename):
                        os.remove(filename)
                    
                    else:
                        print("no file exist")
                candidatedocob.delete()
                logger.info("deleted Sucessfully")
                return Response("deleted Sucessfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return  Response(e,status=status.HTTP_400_BAD_REQUEST)