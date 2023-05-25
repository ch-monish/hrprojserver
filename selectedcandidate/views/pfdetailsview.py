import traceback
from rest_framework.response import Response
from rest_framework import status
from candidate.models.selected_Candidates_Model import  Selected_Candidates
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from selectedcandidate.models.Candidatepfdetails import CandidatePfDetails
from selectedcandidate.Serializers import candidatePFdetailgetSerializer
from django.conf import settings
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils


import logging
from jobpost.models.jobpoststakeholders import JobPostStakeHolders

logger = logging.getLogger(__name__)
class PFdetailsview(ModelViewSet):
    @action(detail=True,methods=["post"])
    def createPFdetail(self,request,format=None):
        try:
            # CandidatePersonalInfo.objects.all()
            selectedcandidateob=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first()
            emails = JobPostStakeHolders.objects.filter(JobPostId=selectedcandidateob.candidate.Jobpost.JobPostId).first()
            try:
                PassportNumber = request.data["PassportNumber"],
            except Exception as e:
                PassportNumber = None,
            try:
                PassportValidFrom = request.data["strPassportValidFrom"],
            except Exception as e:
                PassportValidFrom = None,
            try:
                PassportValidTill = request.data["strPassportValidTill"],
            except Exception as e:
                PassportValidTill = None,
            CandidatePfDetails.objects.create(
            selectedcandidateid=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
            PreviousCompanyUAN = request.data["PreviousCompanyUAN"],
            PreviousMemberId = request.data["PreviousMemberId"],
            MemberNameAsPerAadhar = request.data["MemberNameAsPerAadhar"],
            AADHAR = request.data["AADHAR"],
            DateOfBirth = request.data["strDateOfBirth"],
            Date_Of_Joining = request.data["strDate_Of_Joining"],
            Gender = request.data["Gender"],
            FatherOrHusbandName = request.data["FatherOrHusbandName"],
            Relation = request.data["Relation"],
            Marital_status = request.data["Marital_status"],
            InternationalWorker = request.data["InternationalWorker"],
            ContactNumber = request.data["ContactNumber"],
            Email = request.data["Email"],
            Nationality = request.data["Nationality"],
            # wages = request.data["wages"],
            Qualification = request.data["Qualification"],
            CountryOfOrigin = request.data["CountryOfOrigin"],
            PassportNumber=PassportNumber,
            PassportValidFrom=PassportValidFrom,
            PassportValidTill=PassportValidTill,

            PhysicalHandicap = request.data["PhysicalHandicap"],
            AccountNumber = request.data["AccountNumber"],
            IFSCcode = request.data["IFSCcode"],
            NameAsPerBank = request.data["NameAsPerBank"],
            PAN = request.data["PAN"],
            NameAsPerPan = request.data["NameAsPerPan"],   
            locomotive = request.data["locomotive"],   
            Hearing = request.data["Hearing"],   
            Visual = request.data["Visual"],   
            )

            canmail = selectedcandidateob.OfficialMailId

            subject = 'Candidate '+selectedcandidateob.candidate.CandidateCode+' has been updated the PF details'
            context = {
                'CandidateCode': selectedcandidateob.candidate.CandidateCode,
                'Candidatename': selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName,
                'HRname' : emails.HRName,
                'url' : settings.APP_URL,
            }
            body = EmailUtils.getEmailBody('PF_Details_Updated_template.html', context)
            print("body--"+body)
            print("subject--"+subject)
            print("HREmail--"+emails.HREmail)
            print("canmail--"+canmail)
            EmailUtils.sendEmail(subject, body, [emails.HREmail], [canmail])
           
            logger.info("PF detail created")
            return Response("PF detail created",status=status.HTTP_200_OK)
        
        except Exception as e:
            # print(e)
            logger.error(traceback.format_exc())
            logger.error(e)
            return Response(e,status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=["post"])
    def updatePFdetail(self,request,format=None):
        try:

            CandidatePfDetails.objects.filter(Id=request.data["Id"]).update(
            selectedcandidateid=Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).first(),
            PreviousCompanyUAN = request.data["PreviousCompanyUAN"],
            PreviousMemberId = request.data["PreviousMemberId"],
            MemberNameAsPerAadhar = request.data["MemberNameAsPerAadhar"],
            AADHAR = request.data["AADHAR"],
            DateOfBirth = request.data["strDateOfBirth"],
            Date_Of_Joining = request.data["strDate_Of_Joining"],
            Gender = request.data["Gender"],
            FatherOrHusbandName = request.data["FatherOrHusbandName"],
            Relation = request.data["Relation"],
            Marital_status = request.data["Marital_status"],
            InternationalWorker = request.data["InternationalWorker"],
            ContactNumber = request.data["ContactNumber"],
            Email = request.data["Email"],
            Nationality = request.data["Nationality"],
            # wages = request.data["wages"],
            Qualification = request.data["Qualification"],
            CountryOfOrigin = request.data["CountryOfOrigin"],
            PassportNumber = request.data["PassportNumber"],
            PassportValidFrom = request.data["strPassportValidFrom"],
            PassportValidTill = request.data["strPassportValidTill"],
            PhysicalHandicap = request.data["PhysicalHandicap"],
            AccountNumber = request.data["AccountNumber"],
            IFSCcode = request.data["IFSCcode"],
            NameAsPerBank = request.data["NameAsPerBank"],
            PAN = request.data["PAN"],
            NameAsPerPan = request.data["NameAsPerPan"],  
            locomotive = request.data["locomotive"],   
            Hearing = request.data["Hearing"],   
            Visual = request.data["Visual"],   
            )
            logger.info("PF details updated succesfully")
            return  Response("PF details updated succesfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=["post"])
    def getPFdetails(self,request,format=None):
        try:

            pfdo=CandidatePfDetails.objects.filter(selectedcandidateid=request.data["selectedcandidateid"]).first()
            pfdos=candidatePFdetailgetSerializer(pfdo,many=False).data
            logger.info(pfdos)
            return Response(pfdos,status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)
    
    def deletePFdetail(self,request,format=None):
        try:

            pfdo=CandidatePfDetails.objects.filter(Id=request.data["Id"]).first()
            pfdo.delete()
            logger.info("Deleted Sucessfully")
            return Response("Deleted Sucessfully",status=status.HTTP_200_OK)
        except Exception as e:
             logger.error(e)
             logger.error(traceback.format_exc())
             return Response(e,status=status.HTTP_400_BAD_REQUEST)