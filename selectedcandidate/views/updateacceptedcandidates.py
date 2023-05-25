import traceback
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from candidate.models.selected_Candidates_Model import Selected_Candidates
from jobpost.models.jobpostmodel import JobPost
from managestages.models import Stage
from django.db import transaction
from django.conf import settings
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
import logging

logger = logging.getLogger(__name__)
class Updateacceptedcandidates(ModelViewSet):
    @action(detail=True,methods=["post"])
    def updatefulltimeselectedcandidate(self,request,format=None):
        try:
            with transaction.atomic():
                sendemail = False
                selcanob0=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()
                if(selcanob0.IsJoined is False and request.data["IsJoined"]):
                    sendemail = True
                selcanob=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(
                    HRCID=request.data["HRCID"],
                    EmployeeID=request.data["EmployeeID"],
                    BGVStatus=request.data["BGVStatus"],
                    Medicalteststatus=request.data["Medicalteststatus"],
                    OfficialMailId=request.data["OfficialMailId"],
                    IsJoined=request.data["IsJoined"],
                    Brief_Description=request.data["Brief_Description"],
                    Reportingmanager=request.data["Reportingmanager"]

                )
                # get joined candidates count
                selcanob1=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()
                joinedcandidates =  Selected_Candidates.objects.filter(IsJoined = True, candidate__Jobpost= selcanob1.candidate.Jobpost).count()
                noofpositions  =    JobPost.objects.filter(JobPostId = selcanob1.candidate.Jobpost.JobPostId).first().NoOfPositions
                if joinedcandidates == noofpositions:
                    stage = Stage.objects.filter(StageName=Constants1.STAGE_CLOSED).first() 
                    JobPost.objects.filter(JobPostId = selcanob1.candidate.Jobpost.JobPostId).update(
                        Stage = stage
                    ) 


                
                emails = JobPostStakeHolders.objects.filter(JobPostId=selcanob0.candidate.Jobpost.JobPostId).first()
      
                if(sendemail):
                    #hr in  cc candidate in to sub pf and bank details update
                    canmail = selcanob1.OfficialMailId
                    hrmail=emails.HREmail
                    subject = 'Action: PF and Bank Details Pending'
                    context = {
                        'Candidatename': selcanob1.candidate.CanLastName +", "+ selcanob1.candidate.CanFirstName,
                        'HRname' : emails.HRName,
                        'url' : settings.APP_URL,
                    }
                    body = EmailUtils.getEmailBody('PF_Bank_details_update_template.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("HREmail--"+emails.HREmail)
                    print("canmail--"+canmail)
                    EmailUtils.sendEmail(subject, body, [canmail], [hrmail])  
                logger.info("Candidate Updated Succesfully")                         
                return Response("Candidate Updated Succesfully",status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exeption while updating candidate :"+str(e))
            logger.error(traceback.format_exc())
            return Response("Exeption while updating candidate :"+str(e),status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=["post"])
    def updatecontractselcandidate(self,request,format=None):
        try:
            with transaction.atomic():
                sendemail = False
                selcanob0=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()
                if(selcanob0.IsJoined is False and request.data["IsJoined"]):
                    sendemail = True                
                selcanob=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(
                    HRCID=request.data["HRCID"],
                    EmployeeID=request.data["EmployeeID"],
                    BGVStatus=request.data["BGVStatus"],
                    OfficialMailId=request.data["OfficialMailId"],
                    Medicalteststatus=request.data["Medicalteststatus"],
                    IsJoined=request.data["IsJoined"],
                    Brief_Description=request.data["Brief_Description"],
                    Reportingmanager=request.data["Reportingmanager"]

                )
                # get joined candidates count
                selcanob1=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()
                joinedcandidates =  Selected_Candidates.objects.filter(IsJoined = True, candidate__Jobpost= selcanob1.candidate.Jobpost).count()
                noofpositions  =    JobPost.objects.filter(JobPostId = selcanob1.candidate.Jobpost.JobPostId).first().NoOfPositions
                if joinedcandidates == noofpositions:
                    stage = Stage.objects.filter(StageName=Constants1.STAGE_CLOSED).first() 
                    JobPost.objects.filter(JobPostId = selcanob1.candidate.Jobpost.JobPostId).update(
                        Stage = stage
                    ) 
                emails = JobPostStakeHolders.objects.filter(JobPostId=selcanob0.candidate.Jobpost.JobPostId).first()    
                if(sendemail):
                    #hr in  cc candidate in to sub pf and bank details update
                    canmail = selcanob1.OfficialMailId
                    hrmail=emails.HREmail
                    subject = 'Action: PF and Bank Details Pending'
                    context = {
                        'Candidatename': selcanob1.candidate.CanLastName +", "+ selcanob1.candidate.CanFirstName,
                        'HRname' : emails.HRName,
                        'url' : settings.APP_URL,
                    }
                    body = EmailUtils.getEmailBody('PF_Bank_details_update_template.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("HREmail--"+emails.HREmail)
                    print("canmail--"+canmail)
                    EmailUtils.sendEmail(subject, body, [canmail], [hrmail])                      
                logger.info("Candidate Updated Succesfully")
                return Response("Candidate Updated Succesfully",status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exeption while updating candidate :"+str(e))
            logger.error(traceback.format_exc())
            return Response("Exeption while updating candidate :"+str(e),status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=["post"])
    def updateinternselcandidate(self,request,format=None):
        try:
            with transaction.atomic():
                sendemail = False
                selcanob0=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()
                if(selcanob0.IsJoined is False and request.data["IsJoined"]):
                    sendemail = True                   
                selcanob=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(
                    HRCID=request.data["HRCID"],
                    EmployeeID=request.data["EmployeeID"],
                    BGVStatus=request.data["BGVStatus"],
                    OfficialMailId=request.data["OfficialMailId"],
                    Medicalteststatus=request.data["Medicalteststatus"],
                    IsJoined=request.data["IsJoined"],
                    Brief_Description=request.data["Brief_Description"],
                    Reportingmanager=request.data["Reportingmanager"]

                )
                # get joined candidates count
                selcanob1=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()
                joinedcandidates =  Selected_Candidates.objects.filter(IsJoined = True, candidate__Jobpost= selcanob1.candidate.Jobpost).count()
                noofpositions  =    JobPost.objects.filter(JobPostId = selcanob1.candidate.Jobpost.JobPostId).first().NoOfPositions
                if joinedcandidates == noofpositions:
                    stage = Stage.objects.filter(StageName=Constants1.STAGE_CLOSED).first() 
                    JobPost.objects.filter(JobPostId = selcanob1.candidate.Jobpost.JobPostId).update(
                        Stage = stage
                    ) 
                emails = JobPostStakeHolders.objects.filter(JobPostId=selcanob0.candidate.Jobpost.JobPostId).first()    
                if(sendemail):
                    #hr in  cc candidate in to sub pf and bank details update
                    canmail = selcanob1.OfficialMailId
                    hrmail=emails.HREmail
                    subject = 'Action: PF and Bank Details Pending'
                    context = {
                        'Candidatename': selcanob1.candidate.CanLastName +", "+ selcanob1.candidate.CanFirstName,
                        'HRname' : emails.HRName,
                        'url' : settings.APP_URL,
                    }
                    body = EmailUtils.getEmailBody('PF_Bank_details_update_template.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("HREmail--"+emails.HREmail)
                    print("canmail--"+canmail)
                    EmailUtils.sendEmail(subject, body, [canmail], [hrmail])                      
                logger.info("Candidate Updated Succesfully")
                return Response("Candidate Updated Succesfully",status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exeption while updating candidate :"+str(e))
            logger.error(traceback.format_exc())
            return Response("Exeption while updating candidate :"+str(e),status=status.HTTP_400_BAD_REQUEST)
        
