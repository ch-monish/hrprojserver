import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status  
from rest_framework.response import Response
from jobpost.models.jobpostactionmodel import JobPostActionModel

from jobpost.models.jobpostapprovalmodel import JobPostApproval
from jobpost.models.jobpostmodel import JobPost
from jobpost.serializers import JobPostActionGridSerializer, JobPostActionModelSerializer, JobPostApprovalSerializer, JobPostDetailsGridSerializer, JobPostDetailsPostSerializer
from datetime import datetime

from managestages.models import Stage
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from django.conf import settings
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
import logging

# Create your views here.
logger = logging.getLogger(__name__)
class JobPostAction(ModelViewSet):
    @action(detail=True, methods=['post'])
    def jobpostactiondetails(self, request, format=None):  
       
        try:
            print(request.data)   
            jobPostActionModel = JobPostActionModel.objects.filter(ApproverName=request.data["ApproverName"]).order_by("id").reverse()
            JobPostActionModel_serializer = JobPostActionModelSerializer(jobPostActionModel, many=True)
            # logger.info(JobPostActionModel_serializer.data)
            return Response(JobPostActionModel_serializer.data)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        
        # return Response(JobPostActionModel_serializer.errors.values(), status=status.HTTP_400_BAD_REQUEST) 
    @action(detail=True, methods=['post'])
    def jobpostactionsubmit(self, request, format=None): 
        jobPostApprovalId =  request.data['JobPostApprovalId']
        jobPostId =  request.data['JobPostId']
        approvalStatus =  request.data['ApprovalStatus']
        approvalComments =  request.data['ApprovalComments']
        response = ''
        
        logger.info("Jobpost approval time")     

        try:
            with transaction.atomic():
                jobPostApproval =  JobPostApproval.objects.filter(jobPostApprovalId=jobPostApprovalId).update(
                    approvalDate = datetime.now(),
                    approvalStatus = approvalStatus,
                    approvalComments = approvalComments,
                )

                jobpost =  JobPost.objects.filter(JobPostId=jobPostId).first()
                emails = JobPostStakeHolders.objects.filter(JobPostId=jobPostId).first()
                # JobPostApproval_serializer = JobPostApprovalSerializer(jobPostApproval)
                # if JobPostApproval_serializer.is_valid():
                #     jobPostApprovalupdated = JobPostApproval_serializer.save()
                if jobPostApproval is not None:
                    if (approvalStatus == Constants1.STAGE_A):                
                        stage = Stage.objects.filter(StageName=Constants1.STAGE_PP).first()
                        logger.info(Messages1.JP_APP_SCFL)
                        response = Messages1.JP_APP_SCFL 

                    elif (approvalStatus == Constants1.STAGE_R):
                        stage = Stage.objects.filter(StageName=Constants1.STAGE_R).first()
                        logger.info(Messages1.JP_RJCTD)
                        response = Messages1.JP_RJCTD

                    # print(stage.StageId)
                    count =  JobPost.objects.filter(JobPostId=jobPostId).update(
                        Stage =  stage   
                    )

                    print(count)
                    # return Response(response, status=status.HTTP_200_OK)    
                    
                if jobPostApproval is not None:
                    jobpostdetails_serializer = JobPostDetailsGridSerializer(jobpost)
                    if (approvalStatus == Constants1.STAGE_A):

                        recruitermail = emails.RecruiterEmail
                        hiringmanagermail = emails.HMemail
                        businessheadmail = emails.BHemail
                        subject = 'Action: Upload candidate profiles with respect to the Job Post '+jobpost.JobCode
                        context = {
                            'jobcode': jobpost.JobCode,
                            'recruitername' : emails.RecruiterName,
                            'hiringmanager' : emails.HMname,
                            'businesshead' : emails.BHname,
                            'url' : settings.APP_URL,
                            'jobdetails' : jobpostdetails_serializer.data,
                            "jobdesc" : jobpost.JobDesc.split('\n'),
                            "onboardingdate" : (jobpost.OnBoardingDate).strftime('%m/%d/%Y'),
                            "approvalComments" : approvalComments.split('\n')
                        }
                        body = EmailUtils.getEmailBody('HR_ProfilesUpload_template.html', context)
                        print(body)
                        print(subject)
                        print(recruitermail)
                        print(hiringmanagermail)
                        print(businessheadmail)  
                        EmailUtils.sendEmail(subject, body, [recruitermail], [hiringmanagermail, businessheadmail])

                        stage = Stage.objects.filter(StageName=Constants1.STAGE_PP).first()
                        logger.info(Messages1.JP_APP_SCFL)
                        response = Messages1.JP_APP_SCFL 

                    elif (approvalStatus == Constants1.STAGE_R):
                        
                        recruitermail = emails.RecruiterEmail
                        hiringmanagermail = emails.HMemail
                        businessheadmail = emails.BHemail
                        subject = 'FYI: Job Post '+jobpost.JobCode+' has been rejected'
                        context = {
                            'jobcode': jobpost.JobCode,
                            'hiringmanager' : emails.HMname,
                            'businesshead' : emails.BHname,
                            'url' : settings.APP_URL,
                            'jobdetails' : jobpostdetails_serializer.data,
                            "jobdesc" : jobpost.JobDesc.split('\n'),
                            "onboardingdate" : (jobpost.OnBoardingDate).strftime('%m/%d/%Y'),
                            "approvalComments" : approvalComments.split('\n')
                        }
                        body = EmailUtils.getEmailBody('BusinessHead_JP_Rejection_template.html', context)
                        print(body)
                        print(subject)
                        print(hiringmanagermail)
                        print(businessheadmail)  
                        EmailUtils.sendEmail(subject, body, [hiringmanagermail], [businessheadmail])

                        stage = Stage.objects.filter(StageName=Constants1.STAGE_R).first()
                    logger.info(Messages1.JP_RJCTD)
                        # response = Messages1.JP_RJCTD
                    return Response(response, status=status.HTTP_200_OK)    
                            
                #     jobpost.Stage = stage                
                #     JobPostDetailsPost_serializer = JobPostDetailsPostSerializer(jobpost)
                #     if JobPostDetailsPost_serializer.is_valid():
                #         JobPostDetailsPost_serializer.save()
                #         return Response("Submitted Successfully")
                #     return Response("Exception while approve the job post details"+str(JobPostDetailsPost_serializer.errors), status=status.HTTP_400_BAD_REQUEST) 
                # return Response(JobPostApproval_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as exp:
            logger.error(Messages1.ERR_APP_JP_DTLS+str(exp))
            logger.error(traceback.format_exc())
            return Response(Messages1.ERR_APP_JP_DTLS+str(exp), status=status.HTTP_400_BAD_REQUEST)        