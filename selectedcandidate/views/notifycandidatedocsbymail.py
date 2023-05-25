import base64
import os
from smtplib import SMTPResponseException
import traceback
from candidate.models.selected_Candidates_Model import Selected_Candidates
from rest_framework.response import Response
from rest_framework import status
from candidate.models.selected_Candidates_Model import Selected_Candidates
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from selectedcandidate.models.Candidatedducationaldetails import CandidateEducationalDetails
from selectedcandidate.models.Documentsupload import CandidateDocumentsUpload
from selectedcandidate.Serializers import Documentuploadserializer
from selectedcandidate.Serializers import CandidatedocumentsSerializer
from selectedcandidate.models import *
from candidate.models.selected_Candidates_Model import Selected_Candidates
from HRproj.settings import MEDIA_ROOT, MEDIA_URL, BASE_DIR
from django.http import HttpResponse, Http404
from rest_framework import status
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from django.conf import settings
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
class Notifycandidatedocsbymail(ModelViewSet):
    @action(detail=True,methods=["post"])
    def notifycandidatedocsbymail(self,request,format=None):
        try:
            with transaction.atomic():
                selectedcandidateid = request.data["selectedcandidateid"]       

                selectedcandidateob = Selected_Candidates.objects.filter(Selected_Candidate_ID=selectedcandidateid).first()
                
                emails = JobPostStakeHolders.objects.filter(JobPostId=selectedcandidateob.candidate.Jobpost.JobPostId).first()
                          
                canmail = selectedcandidateob.candidate.Email
      
                subject = 'Verification failled: Re-upload the documents as per rejection comments'
                context = {
                    'Candidatename': selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName,
                    'url' : settings.APP_URL,
                }
                body = EmailUtils.getEmailBody('Can_Notification_template.html', context)
                print("body--"+body)
                print("subject--"+subject)
                print("HREmail--"+emails.HREmail)
                print("canmail--"+canmail)
                EmailUtils.sendEmail(subject, body, [canmail], [emails.HREmail])

            Selected_Candidates.objects.filter(Selected_Candidate_ID=selectedcandidateid).update(
                VerificationStatus="rejected"
            )        
            logger.info("Notification has been sent successfully")
            return Response("Notification has been sent successfully", status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception while sending the notification :  "+str(e))
            logger.error(traceback.format_exc())
            return Response("Exception while sending the notification :  "+str(e), status=status.HTTP_400_BAD_REQUEST)