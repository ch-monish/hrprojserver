import traceback
from rest_framework.response import Response
from rest_framework import status
from candidate.models.selected_Candidates_Model import  Selected_Candidates
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from selectedcandidate.models.Candidatebankdetails import CandidateBankDetails
from selectedcandidate.Serializers import candidatebankdetailgetSerializer
from selectedcandidate.Serializers import bankdetailupdaeSerializer
from django.conf import settings
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils


import logging
from jobpost.models.jobpoststakeholders import JobPostStakeHolders


logger = logging.getLogger(__name__)

class bankdetailsview(ModelViewSet):
    @action(detail=True,methods=["post"])
    def createbankdetail(self,request,format=None):
        try:
            # CandidatePersonalInfo.objects.all()
            selectedcandidateob=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()
            emails = JobPostStakeHolders.objects.filter(JobPostId=selectedcandidateob.candidate.Jobpost.JobPostId).first()

            CandidateBankDetails.objects.create(
            selectedcandidateid=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
            BankName=request.data["BankName"],
            AccountNumber=request.data["AccountNumber"],
            BranchName=request.data["BranchName"],
            IFSCcode=request.data["IFSCcode"],
            BankPassbook=request.data["BankPassbook"],
            )
            #send mail to hr
                
            canmail = selectedcandidateob.OfficialMailId

            subject = 'Candidate '+selectedcandidateob.candidate.CandidateCode+' has been updated the bank details'
            context = {
                'CandidateCode': selectedcandidateob.candidate.CandidateCode,
                'Candidatename': selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName,
                'HRname' : emails.HRName,
                'url' : settings.APP_URL,
            }
            body = EmailUtils.getEmailBody('Bank_Details_Update_template.html', context)
            logger.info("body--"+body)
            logger.info("subject--"+subject)
            logger.info("HREmail--"+emails.HREmail)
            logger.info("canmail--"+canmail)
            EmailUtils.sendEmail(subject, body, [emails.HREmail], [canmail])
            
            logger.info("Bank detail created")    
            return Response("Bank detail created",status=status.HTTP_200_OK)
        
        except Exception as e:
            # logger.info(e)
            logger.error(e)
            logger.error(traceback.format_exc())
            return Response(e,status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=["post"])
    def updatebankdetail(self,request,format=None):
        try:
            # CandidateBankDetails.objects.filter(Id=request.data["Id"]).update(
            #    selectedcandidateid=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
            #    BankName=request.data["BankName"],
            #    AccountNumber=request.data["AccountNumber"],
            #    BranchName=request.data["BranchName"],
            #    IFSCcode=request.data["IFSCcode"],
            #    # hasbankpassbook =False if request.data["BankPassbook"] is None else True
            #    BankPassbook=request.data["BankPassbook"] if request.data["BankPassbook"] is not  None else logger.info() 
            #    # BankPassbook=request.data["BankPassbook"],
            
            # )
            bankdetails=CandidateBankDetails.objects.filter(Id=request.data["Id"]).first()
            # if request.data["BankPassbook"] is None:
            #     bankdetailupdateserializer=candidatebankdetailupdateSerializer(bankdetails,data=request.data)
            # else:
            bankdetailupdateserializer=bankdetailupdaeSerializer(bankdetails,data=request.data)
            if bankdetailupdateserializer.is_valid():
                bankdetailupdateserializer.save()
                logger.info("Bank details updated succesfully")
                return  Response("Bank details updated succesfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(str(e))
             logger.error(traceback.format_exc())
             return  Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=["post"])
    def getbankdetails(self,request,format=None):
        try:

            bdo=CandidateBankDetails.objects.filter(selectedcandidateid=request.data["selectedcandidateid"]).first()
            bdos=candidatebankdetailgetSerializer(bdo,many=False).data
            # logger.info(bdos)
            return Response(bdos,status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    def deletebankdetail(self,request,format=None):
        try:

            bdo=CandidateBankDetails.objects.filter(Id=request.data["Id"]).first()
            bdo.delete()
            logger.info("Deleted Sucessfully")
            return Response("Deleted Sucessfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)