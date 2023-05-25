import traceback
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import Group
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from django.contrib.auth.models import User
from candidate.models.candidateapprovalmodel import CandidateApprovalModel
from managestages.models import Stage
from jobpost.models.jobpostuserrolesmodel import JobPostUserRolesModel
from selectedcandidate.models.Candidatepersonalinfo import CandidatePersonalInfo
from decouple import config
import logging
logger = logging.getLogger(__name__)
class EmailUtils():

    def getEmailBody(template, context):
        body = render_to_string(template, context)    
        return body

    def getRoles(candidateid):

        # candidateapproverobHR=JobPostUserRolesModel.objects.filter(RoleName = Constants1.ROLE_HR).first()
        # if candidateapproverobHR is not None:
        #     HRname = candidateapproverobHR.FullName
        #     HRemail = candidateapproverobHR.Email
        # else:
        #     HRname = "" 
        #     HRemail = "" 
        # print(HRname)
        # print(HRemail)

        # candidateapproverobHR=CandidateApprovalModel.objects.filter(Candidate_id=candidateid,Stage=Stage.objects.filter(
        #                     StageName=Constants1.STAGE_HR_INTERVIEW).first()).first()
        # if candidateapproverobHR is not None:
        #     HRemail =candidateapproverobHR.Email
        #     HRname=candidateapproverobHR.LastName+","+candidateapproverobHR.FirstName
        # else:
        #     HRname = "" 
        #     HRemail = "" 

        # print(HRemail)
        # print(HRname)

        candidateapproverobFC=CandidateApprovalModel.objects.filter(Candidate_id=candidateid,Stage=Stage.objects.filter(
                            StageName=Constants1.STAGE_FCA).first()).first()
        if(candidateapproverobFC is not None):
            FCemail =candidateapproverobFC.Email
            FCname=candidateapproverobFC.LastName+","+candidateapproverobFC.FirstName
        else:
            FCname = "" 
            FCemail = "" 
        print(FCemail)
        print(FCname)
        candidateapproverobGM=CandidateApprovalModel.objects.filter(Candidate_id=candidateid,Stage=Stage.objects.filter(
                            StageName=Constants1.STAGE_GMA).first()).first()
        if(candidateapproverobGM is not None):
            GMemail =candidateapproverobGM.Email
            GMname=candidateapproverobGM.LastName+","+candidateapproverobGM.FirstName
        else:
            GMname = "" 
            GMemail = "" 
        print(GMemail)
        print(GMname)

        return(FCemail,FCname,GMemail,GMname)
    
    
    def sendEmail(subject, body, to, cc):
        try:
            if settings.SEND_EMAIL:    
                email = EmailMessage(
                    subject=subject if config('ENVIRONMENT') == 'Prod' else subject+" (Test)",
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=to,            
                    cc=cc,
                 
                )

                email.content_subtype = "html"  # set the content subtype to html
                email.send()   
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise Exception("Exception while sending emails- "+str(ex))

    def sendEmailWithAttachments(subject, body, to, cc,bcc, filepath1, filepath2):
        try:
            if settings.SEND_EMAIL:    
                email = EmailMessage(
                    subject=subject if config('ENVIRONMENT') == 'Prod' else subject+" (Test)",
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=to,            
                    cc=cc,
                    bcc=bcc
                 
                )

                email.content_subtype = "html"  # set the content subtype to html

                # email.attach_file(filepath, "application/pdf")
                if filepath1 is not None:
                    email.attach_file(filepath1)                  
                    # email.attachments.append(filepath1)
                if filepath2 is not None:
                    email.attach_file(filepath2) 
                    # email.attachments.append(filepath2)  
                email.send()   
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise Exception("Exception while sending emails- "+str(ex))                     