import traceback
from django.db import models
from rest_framework.viewsets import ModelViewSet
import os
from candidate.models.selected_Candidates_Model import Selected_Candidates
from rest_framework.response import Response
from selectedcandidate.models.Documentsupload import CandidateDocumentsUpload
from rest_framework import status
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from django.conf import settings
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from managestages.models import Stage
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
class Acceptofferletter(ModelViewSet): 
 def acceptofferletter(self,request,format=None):
        try:
            with transaction.atomic():

                Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(VerificationStatus='pending')
                CandidateDocumentsUpload.objects.filter(selectedcandidate=request.data["selectedcandidateid"],verified=None).update(verified='pending')

                selectedcandidateid = request.data["selectedcandidateid"]
                # Status = request.data["status"]
                Status = Constants1.VERIFY_REUPLOADED_DOCS if Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"],IsOfferAccepted=True).__len__()>0 else Constants1.VERIFY_UPLOADED_DOCS

                selectedcandidateob = Selected_Candidates.objects.filter(Selected_Candidate_ID=selectedcandidateid).first()
                
                emails = JobPostStakeHolders.objects.filter(JobPostId=selectedcandidateob.candidate.Jobpost.JobPostId).first()
                # HRemail,HRname,FCemail,FCname,GMemail,GMname=EmailUtils.getRoles(selectedcandidateob.candidate.CandidateId)
                
                if (Status == Constants1.VERIFY_UPLOADED_DOCS):
                            # EmailUtils.getRoles(candidateid=candidateob.CandidateId)
                            Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(IsOfferAccepted=True)
                            canmail = selectedcandidateob.candidate.Email
                       
                            subject = 'Action: Candidate '+selectedcandidateob.candidate.CandidateCode+ ' documents verification pending'
                            context = {
                                'CandidateCode': selectedcandidateob.candidate.CandidateCode,
                                'Candidatename': selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName,
                                'HRname' : emails.HRName,
                                'url' : settings.APP_URL,
                            }
                            body = EmailUtils.getEmailBody('Can_Docs_Verification_template.html', context)
                            print("body--"+body)
                            print("subject--"+subject)
                            print("HREmail--"+emails.HREmail)
                            print("canmail--"+canmail)
                            EmailUtils.sendEmail(subject, body, [emails.HREmail], [canmail])

                # Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(IsOfferAccepted=True)

                if (Status == Constants1.VERIFY_REUPLOADED_DOCS):
                            # EmailUtils.getRoles(candidateid=candidateob.CandidateId)
                            
                            canmail = selectedcandidateob.candidate.Email
             
                            subject = 'Action: Candidate '+selectedcandidateob.candidate.CandidateCode+' re-uploaded documents verification pending'
                            context = {
                                'CandidateCode': selectedcandidateob.candidate.CandidateCode,
                                'Candidatename': selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName,
                                'HRname' : emails.HRName,
                                'url' : settings.APP_URL,
                            }
                            body = EmailUtils.getEmailBody('Can_Reuploaded_Docs_Verification_template.html', context)
                            print("body--"+body)
                            print("subject--"+subject)
                            print("HREmail--"+emails.HREmail)
                            print("canmail--"+canmail)
                            EmailUtils.sendEmail(subject, body, [emails.HREmail], [canmail])

                
                
                # for i in selectedcandidatedocsobarr:
                #     print(i.file)
                #     if i.verified is None:
                #         i.objects.update(
                #             verified=False
                #         )
            logger.info("Details has been saved successfully")
            return  Response("Details has been saved successfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error("Exception while recording candidate details "+str(e))
             logger.error(traceback.format_exc())
             return  Response("Exception while recording candidate details "+str(e),status=status.HTTP_400_BAD_REQUEST)