
import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from jobpost.models.jobpostapprovalmodel import JobPostApproval

from jobpost.models.jobpostmodel import JobPost
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
from jobpost.serializers import  JobPostApprovalSerializer, JobPostDetailsGridSerializer, JobPostDetailsPostSerializer
from django.http.response import JsonResponse
from rest_framework import status  
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.db import transaction
import logging
from managestages.models import Stage
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from datetime import datetime

# Create your views here.

logger = logging.getLogger(__name__)
class JobPostApi(APIView):

    def put(self, request, format=None):
        logger.info("Jobpost update start")     
 
        try:
            with transaction.atomic():        
                jobpost =  JobPost.objects.get(JobPostId=request.data['JobPostId'])
                # jobpost.ModifiedBy = ""
                jobpost.ModifiedOn = datetime.now()
                jobpost.ModifiedBy = request.data['UserName']
                JobPostDetailsPost_serializer = JobPostDetailsPostSerializer(jobpost ,data=request.data)
                if JobPostDetailsPost_serializer.is_valid():
                    jobpost1 = JobPostDetailsPost_serializer.save()
                    if jobpost1 is not None:
                        success = self.insertorupdatejobpostapproval(jobpost1, request.data)
                        if success == True:
                            # send email to business head.
                            industryverticalheademail = None 
                            cc = []  
                            # body = render_to_string('businessheadjobpostapproval_template.html', context)
                            jobposttemp =  JobPost.objects.get(JobPostId=jobpost1.JobPostId)
                            jobpostdetails_serializer = JobPostDetailsGridSerializer(jobposttemp)                            
                            BHUserName =  request.data["BH_User_Name"]       
                            BHuser = User.objects.get(username=BHUserName)
                            # Industry Vertical Head
                            jobpoststakeholders =    JobPostStakeHolders.objects.filter(JobPostId = jobpost1.JobPostId).first()
                            if jobpoststakeholders is not None:
                                industryverticalhead = jobpoststakeholders.IndustryHeadusername
                                try:
                                    industryverticalheaduser = User.objects.get(username=industryverticalhead)
                                except User.DoesNotExist:
                                    industryverticalheaduser = None 
                                if industryverticalheaduser is not None:
                                   industryverticalheademail = industryverticalheaduser.email 
                            subject = 'Action: Job Post- '+jobpost1.JobCode+' has been updated and awaiting for approval'
                            context = {
                                'jobcode': jobpost1.JobCode,
                                'hiringmanager' : jobpost1.LastName+", "+jobpost1.FirstName,
                                'url' : settings.APP_URL,
                                'approvername' : BHuser.last_name+", "+BHuser.first_name,
                                'jobdetails' : jobpostdetails_serializer.data,
                                "jobdesc" : jobpost1.JobDesc.split('\n'),
                                "onboardingdate" : datetime.strptime(jobpost1.OnBoardingDate, '%Y-%m-%d').strftime('%m/%d/%Y')
                            }
                            body = EmailUtils.getEmailBody('BusinessHead_JP_Submit_template.html', context)
                            logger.info("Body--"+body)
                            logger.info("subject--"+subject)
                            logger.info("businessheademail--"+BHuser.email)
                            logger.info("hiringmanageremail--"+jobpost1.Email)
                            logger.info("industryverticalheademail--"+str(industryverticalheademail))
                            cc.append(jobpost1.Email)
                            if industryverticalheademail is not None:
                                cc.append(industryverticalheademail)
                            # send_mail(
                            #     subject,
                            #     message=body,
                            #     recipient_list=[BHuser.email],
                            #     from_email=settings.DEFAULT_FROM_EMAIL,
                            #     fail_silently=False,
                            # )  
                            # if settings.SEND_EMAIL:    
                            #     email = EmailMessage(
                            #                 subject=subject,
                            #                 body=body,
                            #                 from_email=settings.DEFAULT_FROM_EMAIL,
                            #                 to=[BHuser.email],            
                            #                 cc=[jobpost1.Email]
                            #     )

                            #     email.content_subtype = "html"  # set the content subtype to html
                            #     email.send()   
                            EmailUtils.sendEmail(subject, body, [BHuser.email], cc)
                    
                    logger.info(Messages1.UPD_SCFL)           
                    return Response(Messages1.UPD_SCFL)
                logger.info(JobPostDetailsPost_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(JobPostDetailsPost_serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as exp:
            # exp.with_traceback()
            logger.error(Messages1.ERR_CRTG_JP+str(exp))
            logger.error(traceback.format_exc())
            return Response(Messages1.ERR_CRTG_JP+str(exp), status=status.HTTP_400_BAD_REQUEST)        

    # @transaction.atomic
    def post(self, request, format=None):
        logger.info("Jobpost add start")
        # company_data = JSONParser().parse(request)
        try:
            with transaction.atomic():
                JobPostDetailsPost_serializer = JobPostDetailsPostSerializer(data=request.data)    
                if JobPostDetailsPost_serializer.is_valid():
                    jobpost1 = JobPostDetailsPost_serializer.save()
                    if jobpost1 is not None:                             
                        success = self.insertorupdatejobpostapproval(jobpost1, request.data)
                        if success == True:
                            # send email to business head.
                            industryverticalheademail = None 
                            cc = []   
                            # body = render_to_string('businessheadjobpostapproval_template.html', context)
                            jobpost =  JobPost.objects.get(JobPostId=jobpost1.JobPostId)
                            jobpostdetails_serializer = JobPostDetailsGridSerializer(jobpost)
                            logger.info(jobpostdetails_serializer.data)
                            BHUserName =  request.data["BH_User_Name"]       
                            BHuser = User.objects.get(username=BHUserName)
                            # Industry Vertical Head
                            jobpoststakeholders =    JobPostStakeHolders.objects.filter(JobPostId = jobpost1.JobPostId).first()
                            if jobpoststakeholders is not None:
                                industryverticalhead = jobpoststakeholders.IndustryHeadusername
                                try:
                                    industryverticalheaduser = User.objects.get(username=industryverticalhead)
                                except User.DoesNotExist:
                                    industryverticalheaduser = None   
                                if industryverticalheaduser is not None:
                                   industryverticalheademail = industryverticalheaduser.email 
                            subject = 'Action: Job Post- '+jobpost1.JobCode+' awaiting for approval'
                            context = {
                                'jobcode': jobpost1.JobCode,
                                'hiringmanager' : jobpost1.LastName+", "+jobpost1.FirstName,
                                'url' : settings.APP_URL,
                                'approvername' : BHuser.last_name+", "+BHuser.first_name,
                                'jobdetails' : jobpostdetails_serializer.data,
                                "jobdesc" : jobpost1.JobDesc.split('\n'),
                                "onboardingdate" : datetime.strptime(jobpost1.OnBoardingDate, '%Y-%m-%d').strftime('%m/%d/%Y')
                            }
                            body = EmailUtils.getEmailBody('BusinessHead_JP_Submit_template.html', context)
                            logger.info("Body--"+body)
                            logger.info("subject--"+subject)
                            logger.info("businessheademail--"+BHuser.email)
                            logger.info("hiringmanageremail--"+jobpost1.Email)
                            logger.info("industryverticalheademail--"+str(industryverticalheademail))
                            cc.append(jobpost1.Email)
                            if industryverticalheademail is not None:
                                cc.append(industryverticalheademail)
                            # send_mail(
                            #     subject,
                            #     message=body,
                            #     recipient_list=[BHuser.email],
                            #     from_email=settings.DEFAULT_FROM_EMAIL,
                            #     fail_silently=False,
                            # )  
                            # if settings.SEND_EMAIL:    
                            #     email = EmailMessage(
                            #                 subject=subject,
                            #                 body=body,
                            #                 from_email=settings.DEFAULT_FROM_EMAIL,
                            #                 to=[BHuser.email],            
                            #                 cc=[jobpost1.Email]
                            #     )

                            #     email.content_subtype = "html"  # set the content subtype to html
                            #     email.send()                      
                            EmailUtils.sendEmail(subject, body, [BHuser.email], cc)
                    # return Response({"status": "success", "data": company_serializer.data}, status=status.HTTP_200_OK)  
                            logger.info(Messages1.JP_CRTD_SCFL)
                            return Response(Messages1.JP_CRTD_SCFL, status=status.HTTP_200_OK)
                        else:
                            logger.info(Messages1.JP_CRTN_FAIL)
                            return Response(Messages1.JP_CRTN_FAIL, status=status.HTTP_400_BAD_REQUEST)
                logger.info(JobPostDetailsPost_serializer.errors)   
                return Response(JobPostDetailsPost_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        except Exception as exp:
            # exp.with_traceback()
            logger.error(Messages1.ERR_CRTG_JP+str(exp))
            logger.error(traceback.format_exc())
            return Response(Messages1.ERR_CRTG_JP+str(exp), status=status.HTTP_400_BAD_REQUEST)
        # return Response("Exception while creation Job Post", status=status.HTTP_400_BAD_REQUEST)
        finally:
            logger.info("Jobpost add end")

    def insertorupdatejobpostapproval(self, jobpost1, data):
        success = True
        try:
            BHUserName =  data["BH_User_Name"]
            HRUserName =  data["HR_User_Name"]

            BHuser = User.objects.get(username=BHUserName)
            BHstage = Stage.objects.filter(StageName=Constants1.STAGE_JP_BHA).first()
            BHrole = Group.objects.filter(name=Constants1.ROLE_BH).first()

            HRuser = User.objects.get(username=HRUserName)
            HRstage = Stage.objects.filter(StageName=Constants1.STAGE_PP).first()
            HRrole = Group.objects.filter(name=Constants1.ROLE_RECRUITER).first()  
            if (BHuser is not None and BHstage is not None and BHrole is not None):
                jobpostapprovalBH = JobPostApproval.objects.filter(jobpost= jobpost1, Stage=BHstage, role=BHrole).first()
                if jobpostapprovalBH is not None:
                    jobpostapprovalreturn = JobPostApproval.objects.filter(jobpost= jobpost1, Stage=BHstage, role=BHrole).update(
                    # jobPostApprovalId = jobpostapprovalBH.jobPostApprovalId,    
                    jobpost = jobpost1,
                    approverName =  BHuser.username,
                    FirstName = BHuser.first_name,
                    LastName = BHuser.last_name,
                    Email = BHuser.email,
                    Stage = BHstage,
                    role = BHrole,
                    approvalStatus = Constants1.NA,
                    approvalDate = None,
                    approvalComments = None,
                    CreatedOn = datetime.now())
                else:
                    jobpostapprovalreturn = JobPostApproval.objects.create(
                    jobpost = jobpost1,
                    approverName =  BHuser.username,
                    FirstName = BHuser.first_name,
                    LastName = BHuser.last_name,
                    Email = BHuser.email,
                    Stage = BHstage,
                    role = BHrole,
                    approvalStatus = Constants1.NA,
                    approvalDate = None,
                    approvalComments = None,
                    CreatedOn = datetime.now())         

            if (HRuser is not None and HRstage is not None and HRrole is not None):
                jobpostapprovalHR = JobPostApproval.objects.filter(jobpost= jobpost1, Stage=HRstage, role=HRrole).first()
                if jobpostapprovalHR is not None:
                    jobpostapprovalreturn = JobPostApproval.objects.filter(jobpost= jobpost1, Stage=HRstage, role=HRrole).update(
                    jobpost = jobpost1,
                    approverName =  HRuser.username,
                    FirstName = HRuser.first_name,
                    LastName = HRuser.last_name,
                    Email = HRuser.email,
                    Stage = HRstage,
                    role = HRrole,
                    approvalStatus = Constants1.NA,
                    approvalDate = None,
                    approvalComments = None,
                    CreatedOn = datetime.now())
                else:
                    jobpostapprovalreturn = JobPostApproval.objects.create(
                    jobpost = jobpost1,
                    approverName =  HRuser.username,
                    FirstName = HRuser.first_name,
                    LastName = HRuser.last_name,
                    Email = HRuser.email,
                    Stage = HRstage,
                    role = HRrole,
                    approvalStatus = Constants1.NA,
                    approvalDate = None,
                    approvalComments = None,
                    CreatedOn = datetime.now())
        except:
            success = False
            logger.error(Messages1.ERR_SAVE_APP_DATA)
            raise Exception(Messages1.ERR_SAVE_APP_DATA)
        return success