import base64
import os
from smtplib import SMTPResponseException
import traceback
from candidate.models.selected_Candidates_Model import Selected_Candidates
from operationalmails.models import Operationalmails
from rest_framework.response import Response
from rest_framework import status
from candidate.models.selected_Candidates_Model import Selected_Candidates
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from selectedcandidate.models.Candidatedducationaldetails import CandidateEducationalDetails
from selectedcandidate.models.Documentsupload import CandidateDocumentsUpload
from selectedcandidate.models import *
from candidate.models.selected_Candidates_Model import Selected_Candidates
from HRproj.settings import MEDIA_ROOT, MEDIA_URL, BASE_DIR
from django.http import HttpResponse, Http404
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
class Verifycandidate(ModelViewSet):
    @action(detail=True,methods=["post"])
    def Verifycandidate(self,request,format=None):
        try:
            with transaction.atomic():
                res={
                    'message':"Candidate verified",
                    'errors':[]
                }
                SelectedCandidateob=Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])
                if (CandidateDocumentsUpload.objects.filter(selectedcandidate=request.data["selectedcandidateid"]).exclude(verified="verified").__len__()==0):
                    
                    SelectedCandidateob.VerificationStatus="verified"
                    SelectedCandidateob.save()
                    if (Operationalmails.objects.filter( selectedcandidateid=SelectedCandidateob).__len__() == 0):
                        self.createoperationalemails(SelectedCandidateob)     
                    logger.info("Candidate verified")
                    # return Response("Candidate verified", status=status.HTTP_200_OK)
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    otherdocsob=CandidateDocumentsUpload.objects.filter(selectedcandidate=request.data["selectedcandidateid"]).exclude(verified="verified")
                    for i in otherdocsob:
                        print(i.detailtype)
                        res["message"]="still some documents need to verify"
                        res["errors"].append(i.detailtype+" document(s) verification pending ")
                    # SelectedCandidateob.VerificationStatus=request.data["Verificationstatus"]
                    # SelectedCandidateob.VerificationComments=request.data["VerificationComments"]
                    # SelectedCandidateob.save()
                    logger.info("Notified candidate to change files")
                    return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("failed to verify candidate ")
            logger.error(traceback.format_exc())
            return Response("failed to verify candidate ", status=status.HTTP_400_BAD_REQUEST)
        
    def createoperationalemails(self,selectedcandidateob):

        Operationalmails.objects.create(
            selectedcandidateid=selectedcandidateob,
            mailcategory="BGV",
            mailsent=False,
            mailsentat=None,
            mailssentto=None
        )

        Operationalmails.objects.create(
            selectedcandidateid=selectedcandidateob,
            mailcategory="Medical Test",
            mailsent=False,
            mailsentat=None,
            mailssentto=None
        )
   
        Operationalmails.objects.create(
            selectedcandidateid=selectedcandidateob,
            mailcategory="Account Creation",
            mailsent=False,
            mailsentat=None,
            mailssentto=None
        )
               
        Operationalmails.objects.create(
            selectedcandidateid=selectedcandidateob,
            mailcategory="IT",
            mailsent=False,
            mailsentat=None,
            mailssentto=None
        )
        Operationalmails.objects.create(
            selectedcandidateid=selectedcandidateob,
            mailcategory="Admin",
            mailsent=False,
            mailsentat=None,
            mailssentto=None
        )

        if (selectedcandidateob.candidate.EmploymentType=="Full-Time" ):                 
            Operationalmails.objects.create(
                selectedcandidateid=selectedcandidateob,
                mailcategory="Insurance",
                mailsent=False,
                mailsentat=None,
                mailssentto=None
            )
        Operationalmails.objects.create(
            selectedcandidateid=selectedcandidateob,
            mailcategory="Welcome Mail",
            mailsent=False,
            mailsentat=None,
            mailssentto=None
        )        