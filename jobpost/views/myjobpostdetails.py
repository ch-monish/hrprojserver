import traceback
from django.shortcuts import render
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from managestages.models import Stage
from rest_framework.viewsets import ModelViewSet
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
from jobpost.models.jobpostmodel import JobPost
from jobpost.serializers import JobPostDetailsGridSerializer, JobPostDetailsPostSerializer
from jobpost.models.jobpostapprovalmodel import JobPostApproval
from django.http.response import JsonResponse
from django.conf import settings
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1

from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from rest_framework import status  
from rest_framework.response import Response
import logging
from rest_framework.decorators import action

# Create your views here.
logger = logging.getLogger(__name__)
class MyJobPostDetails(ModelViewSet):
    @action(detail=True, methods=['post'])
    def getmyjobpostdetails(self, request, format=None): 
        Jobposts = JobPost.objects.filter(UserName=request.data["UserName"]).order_by("JobPostId").reverse()
        jobpostdetailsgrid_serializer = JobPostDetailsGridSerializer(Jobposts, many=True)
        # logger.info(jobpostdetailsgrid_serializer.data)
        return Response(jobpostdetailsgrid_serializer.data)
    
    @action(detail=True, methods=['post'])
    def canceljobpost(self, request, format=None): 
        try:
            jobpostobj = JobPost.objects.get(JobPostId = request.data["JobPostId"])
            cancelstage = Stage.objects.filter(StageName=Constants1.STAGE_CANCELLED).first()
            curstage=Stage.objects.filter(Id=jobpostobj.Stage.Id).first().StageDesc
            jobpostdetails_serializer = JobPostDetailsGridSerializer(jobpostobj)
            emails = JobPostStakeHolders.objects.filter(JobPostId=jobpostobj.JobPostId).first()
            jobpostobj.Comments = request.data["Comments"]
            jobpostobj.Stage = cancelstage
            jobpostobj.save()
            #mail send to 
            # based on its candidate stage
            #buhead,recruiter,hr,
            #jobpost stage if buhead pending include bh in mail
            # profiles pending include recruiter
            # Industry vhead include

            
            to=[]
            cc=JobPostStakeHolders.objects.filter(JobPostId=jobpostobj.JobPostId).first().HMemail
            
            if(curstage=='BH Approval Pending'):
                #include bh industryvh
                # jobpostapproverobj=JobPostApproval.objects.filter(jobpost=jobpostobj,Stage=Stage.objects.filter(Id=1)[0].StageDesc)
                # bhemail=JobPostApproval.objects.filter(jobpost=jobpostobj,role=Group.objects.filter(name="Business Head").first()).first().Email
                bhemail=JobPostStakeHolders.objects.filter(JobPostId=jobpostobj.JobPostId).first().BHemail
                indstryvheademail=JobPostStakeHolders.objects.filter(JobPostId=jobpostobj.JobPostId).first().IndustryHeadEmail
                to.append(bhemail)
                to.append(indstryvheademail)

            elif(curstage=='Profiles Pending'):
                #include bh,industryvh,recruiter,hr
                bhemail=JobPostStakeHolders.objects.filter(JobPostId=jobpostobj.JobPostId).first().BHemail
                indstryvheademail=JobPostStakeHolders.objects.filter(JobPostId=jobpostobj.JobPostId).first().IndustryHeadEmail
                recruiteremail=JobPostStakeHolders.objects.filter(JobPostId=jobpostobj.JobPostId).first().RecruiterEmail
                hremail=JobPostStakeHolders.objects.filter(JobPostId=jobpostobj.JobPostId).first().HREmail
                to.append(bhemail)
                to.append(indstryvheademail)
                to.append(recruiteremail)
                to.append(hremail)




            
            subject = 'FYI: Job Post '+jobpostobj.JobCode+' has been Cancelled'
            context = {
                'jobcode': jobpostobj.JobCode,
                'hiringmanager' : emails.HMname,
                'businesshead' : emails.BHname,
                'url' : settings.APP_URL,
                'jobdetails' : jobpostdetails_serializer.data,
                "jobdesc" : jobpostobj.JobDesc.split('\n'),
                "onboardingdate" : (jobpostobj.OnBoardingDate).strftime('%m/%d/%Y'),
                "cancelComments" : jobpostobj.Comments.split('\n')
            }
            body = EmailUtils.getEmailBody('BusinessHead_JP_Cancel_template.html', context)
            print(body)
            print(subject)
            EmailUtils.sendEmail(subject, body, to, cc)
            logger.info(Messages1.JP_CANCEL)



            return Response("Job Post has been cancelled successfully", status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception while cancelling job post "+str(e))
            logger.error(traceback.format_exc())
            return Response("Exception while cancelling job post "+str(e), status=status.HTTP_400_BAD_REQUEST)

