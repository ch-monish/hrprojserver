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
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from django.conf import settings
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from operationalmails.models import Operationalmails
import logging

logger = logging.getLogger(__name__)
class Verifydocument(ModelViewSet):
 def Verifydocument(self,request,format=None):
    try:
        # pending=False
        # rejected=False
        # do = CandidateDocumentsUpload.objects.filter(
        #     id=request.data["fileid"]).update(verified=request.data["verified"])
        candidatedocob= CandidateDocumentsUpload.objects.get(id=request.data["fileid"])
        selcanid=candidatedocob.selectedcandidate_id
        if request.data["verified"]=='verified':
            candidatedocob.verified="verified"
            candidatedocob.verificationcomments=""
            candidatedocob.save()

        else:
            candidatedocob.verified="rejected"
            candidatedocob.verificationcomments=request.data["verificationcomments"]
            candidatedocob.save()

            # selectedcandidateid = request.data["selectedcandidateid"]
            # Status = request.data["status"]

            # selectedcandidateob = Selected_Candidates.objects.filter(SelectedCandidateId=selectedcandidateid).first()
            
            # emails = JobPostStakeHolders.objects.filter(JobPostId=selectedcandidateob.candidate.Jobpost.JobPostId).first()
            # HRemail,HRname,FCemail,FCname,GMemail,GMname=EmailUtils.getRoles(selectedcandidateid=selectedcandidateob.candidate.CandidateId)

            # if (Status == Constants1.REUPLOAD_REJECTED_DOCS):
            #             # EmailUtils.getRoles(candidateid=candidateob.CandidateId)
                        
            #             canmail = selectedcandidateob.candidate.Email
            #             recruitermail = emails.RecruiterEmail
            #             subject = 'Candidate'+selectedcandidateob.candidate.CandidateCode+' verification comments'
            #             context = {
            #                 'CandidateCode': selectedcandidateob.candidate.CandidateCode,
            #                 'Candidatename': selectedcandidateob.candidate.CanFirstName + selectedcandidateob.candidate.CanLastName,
            #                 'recruitername' : emails.RecruiterName,
            #                 'url' : settings.APP_URL,
            #             }
            #             body = EmailUtils.getEmailBody('Can_Docs_Verification_template.html', context)
            #             print(body)
            #             print(subject)
            #             print(canmail)
            #             EmailUtils.sendEmail(subject, body, [canmail], [recruitermail])

        #check all other documents for candidate and update verification status in selected candidate table
        # alldocs=CandidateDocumentsUpload.objects.filter(selectedcandidate=selcanid)
        # for i in alldocs:
        #     if i.verified=="pending":
        #         pending=True
        #         # Selected_Candidates.objects.filter(Selected_Candidate_ID=selcanid).update(
        #         #     VerificationStatus="pending"
        #         # )
        #     if i.verified=="rejected":
        #         rejected=True
        #         # Selected_Candidates.objects.filter(Selected_Candidate_ID=selcanid).update(
        #         #     VerificationStatus="rejected"
        #         # )
        #         break
        # if(pending==True and rejected==False):
        #    Selected_Candidates.objects.filter(Selected_Candidate_ID=selcanid).update(
        #             VerificationStatus="pending"
        #         )
        # if(rejected==True):
        #     Selected_Candidates.objects.filter(Selected_Candidate_ID=selcanid).update(
        #             VerificationStatus="rejected"
        #         )
        # if(pending==False and rejected==False):
        #     Selected_Candidates.objects.filter(Selected_Candidate_ID=selcanid).update(
        #             VerificationStatus="verified"
        #         )
            # selectedcandidateob = Selected_Candidates.objects.filter(Selected_Candidate_ID=selcanid).first()
            ##write if condition for each row before appending
            #add to operational mails table for selected candidate id
            # if (Operationalmails.objects.filter( selectedcandidateid=selectedcandidateob, mailcategory__ne = "Offer Letter").__len__() == 0):
            # if (Operationalmails.objects.filter( selectedcandidateid=selectedcandidateob).__len__() == 0):
            #     # if(selectedcandidateob.candidate.EmploymentType=="Full-Time" or  selectedcandidateob.candidate.EmploymentType=="Contract(direct)"):
            #         # bgvmailcount = Operationalmails.objects.filter( selectedcandidateid=selectedcandidateob, mailcategory="BGV" ).__len__()
            #         # if bgvmailcount == 0:
            #     Operationalmails.objects.create(
            #         selectedcandidateid=selectedcandidateob,
            #         mailcategory="BGV",
            #         mailsent=False,
            #         mailsentat=None,
            #         mailssentto=None
            #     )
            #     # medicalmailcount = Operationalmails.objects.filter( selectedcandidateid=selectedcandidateob, mailcategory="Medical Test" ).__len__()
            #     # if medicalmailcount == 0:
            #     Operationalmails.objects.create(
            #         selectedcandidateid=selectedcandidateob,
            #         mailcategory="Medical Test",
            #         mailsent=False,
            #         mailsentat=None,
            #         mailssentto=None
            #     )
            #     # accountmailcount = Operationalmails.objects.filter( selectedcandidateid=selectedcandidateob, mailcategory="Account Creation" ).__len__()
            #     # if accountmailcount == 0:        
            #     Operationalmails.objects.create(
            #         selectedcandidateid=selectedcandidateob,
            #         mailcategory="Account Creation",
            #         mailsent=False,
            #         mailsentat=None,
            #         mailssentto=None
            #     )
            #     # itmailcount = Operationalmails.objects.filter( selectedcandidateid=selectedcandidateob, mailcategory="IT" ).__len__()
            #     # if itmailcount == 0:                 
            #     Operationalmails.objects.create(
            #         selectedcandidateid=selectedcandidateob,
            #         mailcategory="IT",
            #         mailsent=False,
            #         mailsentat=None,
            #         mailssentto=None
            #     )
            #     Operationalmails.objects.create(
            #         selectedcandidateid=selectedcandidateob,
            #         mailcategory="Admin",
            #         mailsent=False,
            #         mailsentat=None,
            #         mailssentto=None
            #     )
            #     # insurancemailcount = Operationalmails.objects.filter( selectedcandidateid=selectedcandidateob, mailcategory="Insurance" ).__len__()
            #     # if insurancemailcount == 0:    
            #     if (selectedcandidateob.candidate.EmploymentType=="Full-Time" ):                 
            #         Operationalmails.objects.create(
            #             selectedcandidateid=selectedcandidateob,
            #             mailcategory="Insurance",
            #             mailsent=False,
            #             mailsentat=None,
            #             mailssentto=None
            #         )
            #     Operationalmails.objects.create(
            #         selectedcandidateid=selectedcandidateob,
            #         mailcategory="Welcome Mail",
            #         mailsent=False,
            #         mailsentat=None,
            #         mailssentto=None
            #     )        
        #prev pending curent verified status trigger mail
        logger.info("document verification updated")
        return Response("document verification updated", status=status.HTTP_200_OK)
    except Exception as e:
        logger.error("failed to verify document ")
        logger.error(traceback.format_exc())
        return Response("failed to verify document ", status=status.HTTP_400_BAD_REQUEST)