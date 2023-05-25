import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from candidate.models.candidateactionmodel import CandidateActionModel
from candidate.serializers import AddFeedBackSerializer, AddSelectedCandidatesSerializer, CandidateActionModelSerializer, CandidateDetailsGridSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
from candidate.models.candidatemodel import Candidate
from candidate.models.candidateapprovalmodel import CandidateApprovalModel
from datetime import datetime
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from managestages.models import Stage
from django.contrib.auth.models import User, Group
from jobpost.models.jobpostuserrolesmodel import JobPostUserRolesModel
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from django.conf import settings
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
from candidate.models.selected_Candidates_Model import Selected_Candidates
import logging


logger = logging.getLogger(__name__)
class CandidateAction(ModelViewSet):
    @action(detail=True, methods=['post'])
    def candidateactiondetails(self, request, format=None):
        logger.info(request.data)
        CandidateActionModel1 = CandidateActionModel.objects.filter(
            ApproverName=request.data["ApproverName"])
        CandidateActionModel_serializer = CandidateActionModelSerializer(
            CandidateActionModel1, many=True)
        # logger.info(CandidateActionModel_serializer.data)
        return Response(CandidateActionModel_serializer.data)

    @action(detail=True, methods=['post'])
    def candidateworkflowsubmit(self, request, format=None):
        logger.info("Candidate interview starts")
        try:
            with transaction.atomic():
                cc = []
                candidateapprovalid = request.data["candidateapprovalid"]
                candidateid = request.data["candidateid"]
                Status = request.data["status"]
                comments ="" if request.data["comments"] is None else request.data["comments"] 
                try:
                    feedback = request.data["feedback"]
                except:
                    feedback=None
                try:
                    Interviewerreq = request.data["Interviewer"]
                except:
                    Interviewerreq = None
                try:
                    Internalreq = request.data["Internal"]
                except:
                    Internalreq=None
                response = ''
                candidateob = Candidate.objects.filter(
                    CandidateId=candidateid).first()
                
                ca = CandidateApprovalModel.objects.filter(CandidateApprovalId=candidateapprovalid).update(
                    approvalStatus=Status,
                    approvalDate=datetime.now(),
                    approvalComments=comments
                )
                if(Interviewerreq is not None and Internalreq is not None):
                    Candidate.objects.filter(CandidateId=candidateob.CandidateId).update(
                        Interviewer=Interviewerreq,
                        Internal=Internalreq
                    )
                
                # candidate = Candidate.objects.filter(CandidateId=candidateid).first()
                emails = JobPostStakeHolders.objects.filter(JobPostId=candidateob.Jobpost.JobPostId).first()
                FCemail,FCname,GMemail,GMname=EmailUtils.getRoles(candidateid=candidateob.CandidateId)
                candidatedetails_serializer = CandidateDetailsGridSerializer(candidateob)
                if ca is not None:
                    if (Status == Constants1.SELECT_FOR_INTERVIEW):
                        subject = 'Action: Candidate '+candidateob.CandidateCode+' technical interview is pending'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'hiringmanager' : emails.HMname,             
                            'url' : settings.APP_URL,
                            "candidate" : candidatedetails_serializer.data,
                            "approvalComments" : comments.split('\n')
                        }
                        body = EmailUtils.getEmailBody('HiringManager_Interview_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        cc = [emails.RecruiterEmail, emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        EmailUtils.sendEmail(subject, body, [emails.HMemail], cc)


                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_CI).first()
                        logger.info(Messages1.CAN_IP)
                        response = Messages1.CAN_IP

                    elif (Status == Constants1.REJECTED_AT_REVIEW):

                        subject = 'Candidate ' +candidateob.CandidateCode+ ' has been rejected at the time of review by hiring manager'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'hiringmanager' : emails.HMname,
                            'recruitername' : emails.RecruiterName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Rejected_at_review_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        cc = [emails.HMemail, emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)
                        EmailUtils.sendEmail(subject, body, [recruitermail], cc)
                        
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_REJECTED).first()
                        logger.info("Candidate has been rejected at the time of review")
                        response = "Candidate has been rejected at the time of review"                        

                    elif (Status == Constants1.HM_SHORTLISTED):            

                        subject = 'Candidate '+candidateob.CandidateCode+' HR interview is pending'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'HRname': emails.HRName,
                            'hiringmanager' : emails.HMname,
                            'recruitername' : emails.RecruiterName,
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data
                        }
                        body = EmailUtils.getEmailBody('Candidate_ShortlistedforHRInterview_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        cc = [emails.HMemail,emails.RecruiterEmail,emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)
                        EmailUtils.sendEmail(subject, body, [emails.HREmail], cc)

                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_HR_INTERVIEW).first()
                        logger.info("Candidate has been shortlisted for HR interview ")
                        response = "Candidate has been shortlisted for HR interview "

                    elif (Status == Constants1.HM_REJECTED):                        

                        subject = 'Candidate ' +candidateob.CandidateCode+ ' has been rejected at the time of interview'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'hiringmanager' : emails.HMname,
                            'recruitername' : emails.RecruiterName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Rejected_at_Interview_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        cc = [emails.HMemail,emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                        
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_REJECTED).first()
                        logger.info("Candidate has been rejected at technical interview")
                        response = "Candidate has been rejected at technical interview"  

                    elif (Status == Constants1.HM_HOLD):

                        subject = 'Candidate ' +candidateob.CandidateCode+ ' is on hold by hiring manager'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'hiringmanager' : emails.HMname,
                            'recruitername' : emails.RecruiterName,                                  
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Hold_at_Interview_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        cc = [emails.HMemail,emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                        
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                            
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_HM_HOLD).first()
                        success = self.insertnewrow(candidateob, Status)
                        if success == False:
                            raise Exception(
                                "error while creating new row in candidate approval table")
                        else:
                            logger.info("Candidate has been put on hold")
                            response = "Candidate has been put on hold"                         

                    elif (Status == Constants1.HM_FURTHER_REVIEW):

                        hiringmanagermail = emails.HMemail
                        recruitermail = emails.RecruiterEmail
                        subject = 'Candidate ' +candidateob.CandidateCode+ ' has been shortlisted for further review by hiring manager'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'hiringmanager' : emails.HMname,
                            'recruitername' : emails.RecruiterName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                            "Interviewer" : Interviewerreq
                        }   
                        body = EmailUtils.getEmailBody('Candidate_FurtherReviewAtInterview_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        cc = [emails.HMemail,emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                        
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                        
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_FURTHERREVIEW).first()
                        success = self.insertnewrow(candidateob, Status)
                        if success == False:
                            raise Exception(
                                "error while creating new row in candidate approval table")
                        else:
                            logger.info("Candidate has been shortlisted for further review")
                            response = "Candidate has been shortlisted for further review"

                    elif (Status == Constants1.HR_SHORTLISTED):

                        subject = 'Action: Candidate '+candidateob.CandidateCode+ 'has been pending for approval'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,                            
                            'hiringmanager' : emails.HMname,
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                            "Status" : Constants1.HR_SHORTLISTED
                        }
                        body = EmailUtils.getEmailBody('Candidate_Common_Approval_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        cc = [emails.BHemail,emails.HREmail,emails.RecruiterEmail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)   
                        EmailUtils.sendEmail(subject, body, [emails.HMemail], cc)

                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_CHMA).first()
                        logger.info("Candidate has been shortlisted in HR interview")
                        response = "Candidate has been shortlisted in HR interview "

                    elif (Status == Constants1.HR_HOLD):

                        hiringmanagermail = emails.HMemail
                        recruitermail = emails.RecruiterEmail
                        HRmail = emails.HREmail
                        subject = 'Candidate ' +candidateob.CandidateCode+ ' is on hold by HR'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'hiringmanager' : emails.HMname,
                            'recruitername' : emails.RecruiterName, 
                            'hr' : emails.HRName ,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Hold_at_HR_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        cc = [emails.HMemail,emails.BHemail,emails.HREmail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                           
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_HR_HOLD).first()
                        success = self.insertnewrow(candidateob, Status)
                        if success == False:
                            raise Exception(
                                "error while creating new row in candidate approval table")
                        else:
                            logger.info("Candidate has been put on HR hold")
                            response = "Candidate has been put on HR hold"
                    
                    elif (Status == Constants1.HR_REJECTED):

                        subject = 'Candidate ' +candidateob.CandidateCode+ ' has been rejected at the time of HR interview.'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'hiringmanager' : emails.HMname,
                            'HR':emails.HRName,
                            'recruitername' : emails.RecruiterName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data
                        }   
                        body = EmailUtils.getEmailBody('HR_Rejected_At_Interview_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        cc = [emails.HMemail,emails.BHemail,emails.HREmail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                         
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                        
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_REJECTED).first()
                        logger.info("Candidate has been rejected at HR interview")
                        response = "Candidate has been rejected at HR interview"

                    elif (Status == Constants1.HM_CANDIDATE_APPROVAL):
 
                        subject = 'Action: Candidate '+candidateob.CandidateCode+' has been pending for approval'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'businessheadname': emails.BHname,
                            'hiringmanager' : emails.HMname,
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                            "Status" : Constants1.HM_CANDIDATE_APPROVAL
                        }
                        body = EmailUtils.getEmailBody('Candidate_Common_Approval_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        cc = [emails.HMemail,emails.RecruiterEmail,emails.HREmail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                         
                        EmailUtils.sendEmail(subject, body, [emails.BHemail], cc)

                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_BH_CANDIDATE_APPROVAL).first()
                        logger.info("Candidate has been approved by the hiring manager successfully")
                        response = "Candidate has been approved by the hiring manager successfully"    

                    elif (Status == Constants1.HM_CANDIDATE_REJECTED):

                        subject = 'Candidate ' +candidateob.CandidateCode+ ' has been rejected at the time of hiring manager approval.'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'hiringmanager' : emails.HMname,
                            'HRname':emails.HRName,
                            'recruitername' : emails.RecruiterName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                            "Status" : Constants1.HM_CANDIDATE_REJECTED
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Common_Reject_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        cc = [emails.HMemail,emails.BHemail,emails.HREmail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                         
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                        
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_REJECTED).first()
                        logger.info("Candidate has been rejected")
                        response = "Candidate has been rejected"

                    elif (Status == Constants1.BH_CANDIDATE_APPROVAL):

                        if candidateob.NegotiatedCTC is not None and candidateob.AvgApprovedCTC is not None and candidateob.NegotiatedCTC > candidateob.AvgApprovedCTC:

                            success = self.insertnewrow(candidateob, Status)
                            if success == False:
                                raise Exception(
                                    "error while creating new row in candidate approval table")
                            logger.info("Candidate has been approved by the Business Head successfully")
                            response = "Candidate has been approved by the Business Head successfully."
                            
                            FCemail,FCname,GMemail,GMname=EmailUtils.getRoles(candidateid=candidateob.CandidateId)
                            subject = 'Action: Candidate '+candidateob.CandidateCode+' has been pending for approval'
                            context = {
                                'CandidateCode': candidateob.CandidateCode,
                                'financecontrollername' : FCname,                                
                                'url' : settings.APP_URL,
                                "approvalComments" : comments.split('\n'),
                                "candidate" : candidatedetails_serializer.data,
                                "Status" : Constants1.BH_CANDIDATE_APPROVAL
                            }   
                            body = EmailUtils.getEmailBody('Candidate_Common_Approval_template.html', context)
                            logger.info("body--"+body)
                            logger.info("subject--"+subject)
                            logger.info("hiringmanagermail--"+emails.HMemail)
                            logger.info("busniessheadmail--"+emails.BHemail)
                            logger.info("recruitermail--"+emails.RecruiterEmail)
                            # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                            logger.info("HRmail--"+emails.HREmail)
                            logger.info("fincancecontrollermail--"+FCemail)
                            cc = [emails.HMemail,emails.BHemail,emails.HREmail,emails.RecruiterEmail]
                            if emails.IndustryHeadEmail is not None:
                                cc.append(emails.IndustryHeadEmail)                             
                            EmailUtils.sendEmail(subject, body, [FCemail], cc)

                            stage = Stage.objects.filter(
                                StageName=Constants1.STAGE_FC_Approval).first()
                            
                        else:
                            subject = 'Action: Candidate' +candidateob.CandidateCode+ ' offer letter creation request'
                            context = {
                                'CandidateCode': candidateob.CandidateCode,                                
                                'HRname' : emails.HRName,                                
                                'url' : settings.APP_URL,
                                "approvalComments" : comments.split('\n'),
                                "candidate" : candidatedetails_serializer.data,
                            }   
                            body = EmailUtils.getEmailBody('HR_Offer_Letter_Generation_template.html', context)
                            logger.info("body--"+body)
                            logger.info("subject--"+subject)
                            logger.info("hiringmanagermail--"+emails.HMemail)
                            logger.info("busniessheadmail--"+emails.BHemail)
                            logger.info("recruitermail--"+emails.RecruiterEmail)
                            # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                            logger.info("HRmail--"+emails.HREmail)
                            cc = [emails.HMemail,emails.BHemail,emails.RecruiterEmail]
                            if emails.IndustryHeadEmail is not None:
                                cc.append(emails.IndustryHeadEmail)                            
                            EmailUtils.sendEmail(subject, body, [emails.HREmail], cc)
                            stage = Stage.objects.filter(
                                StageName=Constants1.STAGE_SELECTED).first()
                            self.addselectedcandidate(candidateob)
                            logger.info("Candidate has been selected")
                            response = "Candidate has been selected"
                                
                    elif (Status == Constants1.BH_CANDIDATE_REJECTED):

                        subject = 'Candidate ' +candidateob.CandidateCode+ ' has been rejected at the time of business unit head approval.'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'recruitername' : emails.RecruiterName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                            "Status" : Constants1.BH_CANDIDATE_REJECTED
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Common_Reject_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        cc = [emails.HMemail,emails.BHemail,emails.HREmail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                         
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                        
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_REJECTED).first()
                        logger.info("Candidate has been rejected")
                        response = "Candidate has been rejected"                                
                    
                    elif (Status == Constants1.FC_Approval):

                        subject = 'Action: Candidate '+candidateob.CandidateCode+' has been pending for approval'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'generalmanager':GMname,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                            "Status" : Constants1.FC_Approval
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Common_Approval_template.html', context)

                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        logger.info("generalmanagermail--"+GMemail)
                        logger.info("fincancecontrollermail--"+FCemail)
                        cc = [emails.HMemail,FCemail,emails.HREmail,emails.RecruiterEmail,emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                           
                        EmailUtils.sendEmail(subject, body, [GMemail], cc)

                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_GM_Approval).first()
                        logger.info("Candidate has been approved by Finance Controller successfully")
                        response = "Candidate has been approved by Finance Controller successfully"

                    elif (Status == Constants1.FC_Approval_REJECTED):

                        subject = 'Candidate ' +candidateob.CandidateCode+ ' has been rejected at the time of finance controller approval.'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'recruitername' : emails.RecruiterName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                            "Status" : Constants1.FC_Approval_REJECTED
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Common_Reject_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)                        
                        logger.info("fincancecontrollermail--"+FCemail)
                        cc = [emails.HMemail,FCemail,emails.HREmail,emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                            
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                        
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_REJECTED).first()
                        logger.info("Candidate has been rejected")
                        response = "Candidate has been rejected"                           

                    elif (Status == Constants1.GM_Approval):

                        subject = 'Action: Candidate' +candidateob.CandidateCode+ ' offer letter creation request'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'HRname' : emails.HRName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                        }   
                        body = EmailUtils.getEmailBody('HR_Offer_Letter_Generation_template.html', context)

                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        logger.info("generalmanagermail--"+GMemail)
                        logger.info("fincancecontrollermail--"+FCemail)
                        cc = [emails.HMemail,FCemail,GMemail, emails.RecruiterEmail,emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                         
                        EmailUtils.sendEmail(subject, body, [emails.HREmail], cc)
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_SELECTED).first()
                        self.addselectedcandidate(candidateob)
                        logger.info("Candidate has been selected")
                        response = "Candidate has been selected"

                    elif (Status == Constants1.GM_Approval_REJECTED):

                        subject = 'Candidate ' +candidateob.CandidateCode+ ' has been rejected at the time of general manager approval.'
                        context = {
                            'CandidateCode': candidateob.CandidateCode,
                            'recruitername' : emails.RecruiterName,                                
                            'url' : settings.APP_URL,
                            "approvalComments" : comments.split('\n'),
                            "candidate" : candidatedetails_serializer.data,
                            "Status" : Constants1.GM_Approval_REJECTED
                        }   
                        body = EmailUtils.getEmailBody('Candidate_Common_Reject_template.html', context)
                        logger.info("body--"+body)
                        logger.info("subject--"+subject)
                        logger.info("hiringmanagermail--"+emails.HMemail)
                        logger.info("busniessheadmail--"+emails.BHemail)
                        logger.info("recruitermail--"+emails.RecruiterEmail)
                        # logger.info("industryheadmail--"+emails.IndustryHeadEmail)
                        logger.info("HRmail--"+emails.HREmail)
                        logger.info("generalmanagermail--"+GMemail)
                        logger.info("fincancecontrollermail--"+FCemail)
                        cc = [emails.HMemail,FCemail,GMemail, emails.HREmail,emails.BHemail]
                        if emails.IndustryHeadEmail is not None:
                            cc.append(emails.IndustryHeadEmail)                            
                        EmailUtils.sendEmail(subject, body, [emails.RecruiterEmail], cc)
                        
                        stage = Stage.objects.filter(
                            StageName=Constants1.STAGE_REJECTED).first()
                        logger.info("Candidate has been rejected")
                        response = "Candidate has been rejected"  

                    candidatecount = Candidate.objects.filter(CandidateId=candidateid).update(
                        Stage=stage
                    )
                else:
                    raise Exception
                if feedback is not None:
                    logger.info("create bulk insert")
                    logger.info(request.data)
                    serializer = AddFeedBackSerializer(data=feedback,many=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                logger.info(response)
                return Response(response, status=status.HTTP_200_OK)
        except Exception as exp:
            logger.error(traceback.format_exc())
            logger.error(Messages1.ERR_FBK_CAN+str(exp))
            return Response(Messages1.ERR_FBK_CAN+str(exp), status=status.HTTP_400_BAD_REQUEST)
    
    def insertnewrow(self, candidate1, status):
        success = True
        try:
            HMUserName = candidate1.Jobpost.UserName
            HRUserName = ""
            HRUserObj = JobPostUserRolesModel.objects.filter(
                RoleName=Constants1.ROLE_HR).first()
            if HRUserObj is not None:
                HRUserName = HRUserObj.UserName
            else:
                HRUserName = ""
            HRuser = User.objects.get(username=HRUserName)
            HRHoldstage = Stage.objects.filter(
                StageName=Constants1.STAGE_HR_HOLD).first()
            HRrole = Group.objects.filter(name=Constants1.ROLE_HR).first()
            HMUser = User.objects.get(username=HMUserName)
            HMHoldstage = Stage.objects.filter(
                StageName=Constants1.STAGE_HM_HOLD).first()
            HMFurtherReviewstage = Stage.objects.filter(
                StageName=Constants1.STAGE_FURTHERREVIEW).first()
            HMrole = Group.objects.filter(name=Constants1.ROLE_HM).first()


             # Finannce Controller
            FCUserObj =  JobPostUserRolesModel.objects.filter(RoleName = Constants1.ROLE_FC).first()
            if FCUserObj is not None:
                FCUserName = FCUserObj.UserName
            else:
                FCUserName = ""  
            # General Manager
            GMUserObj =  JobPostUserRolesModel.objects.filter(RoleName = Constants1.ROLE_GM).first()
            if GMUserObj is not None:
                GMUserName = GMUserObj.UserName
            else:
                GMUserName = ""  

            GMuser = User.objects.get(username=GMUserName)
            GMApprovalstage = Stage.objects.filter(StageName=Constants1.STAGE_GMA).first()
            GMrole = Group.objects.filter(name=Constants1.ROLE_GM).first() 

            FCuser = User.objects.get(username=FCUserName)
            FCApprovalstage = Stage.objects.filter(StageName=Constants1.STAGE_FCA).first()
            FCrole = Group.objects.filter(name=Constants1.ROLE_FC).first() 


            if status == Constants1.HM_HOLD and HMUser is not None and HMHoldstage is not None and HMrole is not None:
                candidateHMhold = CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=HMHoldstage, role=HMrole).first()
                if candidateHMhold is not None:
                    CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=HMHoldstage, role=HMrole).update(
                        Candidate=candidate1,
                        approverName=HMUser.username,
                        FirstName=HMUser.first_name,
                        LastName=HMUser.last_name,
                        Email=HMUser.email,
                        Stage=HMHoldstage,
                        role=HMrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now()

                    )
                else:    
                    CandidateApprovalModel.objects.create(
                        Candidate=candidate1,
                        approverName=HMUser.username,
                        FirstName=HMUser.first_name,
                        LastName=HMUser.last_name,
                        Email=HMUser.email,
                        Stage=HMHoldstage,
                        role=HMrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now())
            
            if status == Constants1.HM_FURTHER_REVIEW and HMUser is not None and HMFurtherReviewstage is not None and HMrole is not None:
                candidateHMfurtherreview = CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=HMFurtherReviewstage, role=HMrole).first()
                if candidateHMfurtherreview is not None:
                    CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=HMFurtherReviewstage, role=HMrole).update(
                        Candidate=candidate1,
                        approverName=HMUser.username,
                        FirstName=HMUser.first_name,
                        LastName=HMUser.last_name,
                        Email=HMUser.email,
                        Stage=HMFurtherReviewstage,
                        role=HMrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now()

                    )
                else:            
                    CandidateApprovalModel.objects.create(
                        Candidate=candidate1,
                        approverName=HMUser.username,
                        FirstName=HMUser.first_name,
                        LastName=HMUser.last_name,
                        Email=HMUser.email,
                        Stage=HMFurtherReviewstage,
                        role=HMrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now())
            
            if status == Constants1.BH_CANDIDATE_APPROVAL and FCuser is not None and FCApprovalstage is not None and FCrole is not None:
                candidateFCapprover = CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=FCApprovalstage, role=FCrole).first()
                if candidateFCapprover is not None:
                    CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=FCApprovalstage, role=FCrole).update(
                        Candidate=candidate1,
                        approverName=FCuser.username,
                        FirstName=FCuser.first_name,
                        LastName=FCuser.last_name,
                        Email=FCuser.email,
                        Stage=FCApprovalstage,
                        role=FCrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now())
                    
                else:                
                    CandidateApprovalModel.objects.create(
                        Candidate=candidate1,
                        approverName=FCuser.username,
                        FirstName=FCuser.first_name,
                        LastName=FCuser.last_name,
                        Email=FCuser.email,
                        Stage=FCApprovalstage,
                        role=FCrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now())
            
            if status == Constants1.BH_CANDIDATE_APPROVAL and GMuser is not None and GMApprovalstage is not None and GMrole is not None:
                candidateGMapprover = CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=GMApprovalstage, role=GMrole).first()
                if candidateGMapprover is not None:
                    CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=GMApprovalstage, role=GMrole).update(
                        Candidate=candidate1,
                        approverName=GMuser.username,
                        FirstName=GMuser.first_name,
                        LastName=GMuser.last_name,
                        Email=GMuser.email,
                        Stage=GMApprovalstage,
                        role=GMrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now())
                    
                else:                
                    CandidateApprovalModel.objects.create(
                        Candidate=candidate1,
                        approverName=GMuser.username,
                        FirstName=GMuser.first_name,
                        LastName=GMuser.last_name,
                        Email=GMuser.email,
                        Stage=GMApprovalstage,
                        role=GMrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now())
            # if status == Constants1.BH_CANDIDATE_APPROVAL and GMuser is not None and GMApprovalstage is not None and GMrole is not None:
            #     CandidateApprovalModel.objects.create(
            #         Candidate=candidate1,
            #         approverName=GMuser.username,
            #         FirstName=GMuser.first_name,
            #         LastName=GMuser.last_name,
            #         Email=GMuser.email,
            #         Stage=GMApprovalstage,
            #         role=GMrole,
            #         approvalStatus='N',
            #         approvalDate=None,
            #         approvalComments=None,
            #         CreatedOn=datetime.now())
            if status == Constants1.HR_HOLD and HRuser is not None and HRHoldstage is not None and HRrole is not None:
                candidateHRHold = CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=HRHoldstage, role=HRrole).first()
                if candidateHRHold is not None:
                    CandidateApprovalModel.objects.filter(Candidate= candidate1, Stage=HRHoldstage, role=HRrole).update(
                        Candidate=candidate1,
                        approverName=HRuser.username,
                        FirstName=HRuser.first_name,
                        LastName=HRuser.last_name,
                        Email=HRuser.email,
                        Stage=HRHoldstage,
                        role=HRrole,
                        approvalStatus='N',
                        approvalDate=None,
                        approvalComments=None,
                        CreatedOn=datetime.now())
                    
                else:                 
                    CandidateApprovalModel.objects.create(
                    Candidate=candidate1,
                    approverName=HRuser.username,
                    FirstName=HRuser.first_name,
                    LastName=HRuser.last_name,
                    Email=HRuser.email,
                    Stage=HRHoldstage,
                    role=HRrole,
                    approvalStatus='N',
                    approvalDate=None,
                    approvalComments=None,
                    CreatedOn=datetime.now())
            # if status == Constants1.HOLD_AT_HM_INTERVIEW and HMUser is not None and HMHoldstage is not None and HMrole is not None:
            #     CandidateApprovalModel.objects.create(
            #     Candidate = candidate1,
            #     approverName =  HMUser.username,
            #     FirstName = HMUser.first_name,
            #     LastName = HMUser.last_name,
            #     Email = HMUser.email,
            #     Stage = HRHoldstage,
            #     role = HMrole,
            #     approvalStatus = 'N',
            #     approvalDate = None,
            #     approvalComments = None,
            #     CreatedOn = datetime.now())
        except Exception as exp:
            success = False
            logger.error(Messages1.ERR_SAVE_APP_DATA+str(exp))
            logger.error(traceback.format_exc())
            raise Exception(Messages1.ERR_SAVE_APP_DATA+str(exp))
        logger.info(success)
        return success
    
    def addselectedcandidate(self,candidateob):
        # logger.info(candidateob)
        selectedcandidatesvar=Selected_Candidates
        # addselectedcandidatesserializer=AddSelectedCandidatesSerializer(data=candidateob)
       
        try:
            # res= addselectedcandidatesserializer.save(
            if (Selected_Candidates.objects.filter(candidate =candidateob).__len__() == 0):   
                Selected_Candidates.objects.create(
                    candidate=candidateob,
                    # IsOfferAccepted=False,
                    # IsJoined=False,
                    # HRCID=None,
                    # EmployeeID=None,
                    # designation=None,
                    # subband=None,#foerign key
                    # band=None,#foerign key
                    # DateOfJoining=None,
                    # FixedCTC=0,
                    # VariablePay=None,
                    # OfferLetter = None,
                    # MQVariable=None,
                    # FinalCTC=0,
                    # Is_Eligible_annu_Mgnt_Bonus=False,
                    # Is_Eligible_Joining_Bonus=False,
                    # IS_Eligible_Monthly_Incentive=False,
                    Created_By="System",
                    Created_on=datetime.now(),
                    # Modified_By=None,
                    # Modified_On=None,
                )
            
            # create({
            #     candidate=candidateob
            # })
            # if res==True:
            #     return
        except Exception as  e:
            logger.error("Selected Candidate not created :"+str(e))
            logger.error(traceback.format_exc())
            raise  Exception("Selected Candidate not created :"+str(e))

