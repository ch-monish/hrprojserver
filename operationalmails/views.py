import traceback
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from ManageAdUsers.models import AdUsers
from ManageBand.models import Band
from jobpost.models.jobpostmodel import JobPost
from ManageInsurance.models import Insurance
from manageserviceline.models import ServiceLine
from operationalmails.models import Operationalmails
from operationalmails.serializers import operationalMailsSerializer
from candidate.models.selected_Candidates_Model  import Selected_Candidates
from rest_framework import status
from datetime import datetime
import base64
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from HRproj.util.Messages.HR_WorkFlow_Messages import Messages1
from django.conf import settings
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from selectedcandidate.models.Candidateinsurancedetails import CandidateInsuranceDetails
from django.views.generic import TemplateView
from DepartmentInfo.models import DepartmentInformation
from selectedcandidate.models.Candidatedducationaldetails import CandidateEducationalDetails
from selectedcandidate.models.Documentsupload import CandidateDocumentsUpload
import io
import os
from docxtpl import DocxTemplate
from django.core.files.uploadedfile import SimpleUploadedFile
from HRproj.settings import MEDIA_ROOT
from docx2pdf import convert
import random
import string
import locale
from HRproj.settings import MEDIA_ROOT, MEDIA_URL, BASE_DIR
from selectedcandidate.models.Candidatepersonalinfo import CandidatePersonalInfo
from django.db import transaction
import base64
import logging
from html2image import Html2Image
# Create your views here.
logger = logging.getLogger(__name__)
class Operationalmailsview(ModelViewSet):
    @action(methods=['post'],detail=True)
    def getoperationalmails(self,request,format=None):
        try:
            mailsobj=Operationalmails.objects.filter(selectedcandidateid=request.data["selectedcandidateid"])
            mailsserializer =operationalMailsSerializer(mailsobj,many=True)
            # logger.info(mailsserializer.data)
            return Response(mailsserializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("error : "+str(e))
            logger.error(traceback.format_exc())
            return Response("error : "+str(e),status=status.HTTP_400_BAD_REQUEST)
    
    def sendoperationalmail(self,request,format=None):
        try:
            with transaction.atomic(): 
                candphotobase64 = ""
                baseurlbase64 = ""
                mailrowob=Operationalmails.objects.filter(id=request.data["id"]).first()
                # selectedcandidateid = mailrowob.selectedcandidateid
                selectedcandidateob = Selected_Candidates.objects.filter(Selected_Candidate_ID=mailrowob.selectedcandidateid.Selected_Candidate_ID).first()
                insurancedetailsob = CandidateInsuranceDetails.objects.filter(Selected_Candidate_ID=mailrowob.selectedcandidateid.Selected_Candidate_ID)
                insuranceselfob = CandidateInsuranceDetails.objects.filter(Selected_Candidate_ID=mailrowob.selectedcandidateid.Selected_Candidate_ID,Relationship="self").first()
                emails = JobPostStakeHolders.objects.filter(JobPostId=selectedcandidateob.candidate.Jobpost.JobPostId).first()
                personalinfoob=CandidatePersonalInfo.objects.filter(selectedCandidateid=selectedcandidateob.Selected_Candidate_ID).first()
                # selectedcandidateid=selectedcandidateob.candidate.CandidateId
                FCemail,FCname,GMemail,GMname=EmailUtils.getRoles(selectedcandidateob.candidate.CandidateId)
                try:
                    bgvmail=request.data["Bgvvendor"]
                except:
                    bgvmail=""
                selectedcandidateid=mailrowob.selectedcandidateid
                if(mailrowob.mailcategory=="Welcome Mail"):
                    hti = Html2Image(output_path=os.path.join(MEDIA_ROOT, selectedcandidateob.candidate.Jobpost.JobCode, selectedcandidateob.candidate.CandidateCode).replace('\\','/'))
                    #selected candidate table update bgv status
                    # canmail=selectedcandidateob.candidate.Email
                    educationsobj=CandidateEducationalDetails.objects.filter(selectedCandidateId=mailrowob.selectedcandidateid.Selected_Candidate_ID).first()
                    belcanindiagroupmail=DepartmentInformation.objects.filter(Department="Belcan India").first().Email
                    subject = 'Welcome Aboard - '+selectedcandidateob.candidate.CanFirstName
                    canemail=selectedcandidateob.candidate.Email
                    candesignation=selectedcandidateob.designation.DesignationName
                    joblocation=selectedcandidateob.candidate.Location.LocationName
                    qualification=educationsobj.Qualification
                    Institute=educationsobj.Institute
                    Briefdescription=selectedcandidateob.Brief_Description
                    officialmail=selectedcandidateob.OfficialMailId
                    candphoto=os.path.join(MEDIA_ROOT,CandidateDocumentsUpload.objects.filter(selectedcandidate=selectedcandidateob,detailtype="Photograph").first().file.name)
                    print(candphoto)
                    candphoto = candphoto.replace("/", "\\")
                    print(candphoto)
                    baseurl = os.path.join(BASE_DIR, "Welcomebackground.jpg").replace('\\','/')
                    print(baseurl)
                    # 'EmployeeID','Name','DoB','Age','Relation','Gender','Band','GMC coverage(INR)','GPA coverage(INR)','DOJ','Official MailID','Personal Email','Contact Number'
                    with open(candphoto, 'rb') as fh:
                        candphotobase64=base64.b64encode(fh.read()).decode('utf-8')
                    with open(baseurl, 'rb') as fh1:
                        baseurlbase64=base64.b64encode(fh1.read()).decode('utf-8')                        
                    context = {
                        'fullname': selectedcandidateob.candidate.CanFirstName +" "+ selectedcandidateob.candidate.CanLastName,
                        'honofirstname': selectedcandidateob.candidate.Honorifics+"."+selectedcandidateob.candidate.CanFirstName ,
                        'canfirstname': selectedcandidateob.candidate.CanFirstName,
                        'candesignation': candesignation,
                        'joblocation': joblocation,
                        'qualification': qualification,
                        'Institute': Institute,
                        'Briefdescription': Briefdescription.split('\n'),
                        'officialmail': officialmail,
                        # 'candphoto':"data:image/jpeg;base64,"+str(candphotobase64),
                        'candphoto' : candphoto,
                        # 'candphoto':'<img src="data:image/jpeg;base64,' + str(candphotobase64) + '"> </img>',
                        # 'baseurl' :  "data:image/png;base64,"+str(baseurlbase64),
                        # 'baseurl' :   "data:image/png;base64,"+str(baseurlbase64),
                        'baseurl' :   baseurl,
                        'serviceline': selectedcandidateob.candidate.Jobpost.ServiceLine.ServiceLineName,
                        "canlastfirst":selectedcandidateob.candidate.CanLastName+", "+selectedcandidateob.candidate.CanFirstName 
                        
                    }
                    body = EmailUtils.getEmailBody('WelcomeAboard.html', context)
                    print(os.path.join(MEDIA_ROOT, selectedcandidateob.candidate.Jobpost.JobCode, selectedcandidateob.candidate.CandidateCode, "welcomeaboard.png").replace('\\','/'))
                    hti.screenshot(html_str=body, save_as= "welcomeaboard.png")
                    print("body---"+body)
                    print("subject---"+subject)
                    print("belcanindiagroupmail---"+belcanindiagroupmail)
                    print("emails.HREmail---"+emails.HREmail)
                    print("canemail---"+canemail)
                    output_file=os.path.join(MEDIA_ROOT, selectedcandidateob.candidate.Jobpost.JobCode, selectedcandidateob.candidate.CandidateCode, "welcomeaboard.png").replace('\\','/')
                    with open(output_file, 'rb') as fh:
                        welcomebase64=base64.b64encode(fh.read()).decode('utf-8')
                    body1 = "<html> <body> <img src=data:image/png;base64,"+str(welcomebase64)+" > </body> </html>"
                    print("body1---"+body1)
                    EmailUtils.sendEmail(subject, body1, [belcanindiagroupmail], [emails.HREmail,canemail])

                    #send mail code
                    mailrowob.mailsent=True
                    mailrowob.mailsentat=datetime.now()
                    mailrowob.mailssentto=belcanindiagroupmail
                    mailrowob.save()
                
                if(mailrowob.mailcategory=="BGV"):
                    bgvto = []
                    canname = selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName
                    subject = 'Candidate '+canname+' background Verification request'
                    canemail=selectedcandidateob.candidate.Email
                    if bgvmail is not None:
                        bgvto = bgvmail.split(',')
                    # 'EmployeeID','Name','DoB','Age','Relation','Gender','Band','GMC coverage(INR)','GPA coverage(INR)','DOJ','Official MailID','Personal Email','Contact Number'

                    context = {
                        'canname': canname,                                      
                        'canemail' : selectedcandidateob.candidate.Email,
                        'canphoneno' : personalinfoob.ContactNumber,
                        
                    }
                    body = EmailUtils.getEmailBody('BGV_Verification_Mail.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("bgvmail--"+bgvmail)
                    print("bgvto--"+str(bgvto))
                    print("HRemail--"+emails.HREmail)
                    EmailUtils.sendEmail(subject, body, bgvto, [emails.HREmail])

                    #send mail code
                    mailrowob.mailsent=True
                    mailrowob.mailsentat=datetime.now()
                    mailrowob.mailssentto=bgvmail
                    mailrowob.save()
                    Selected_Candidates.objects.filter(Selected_Candidate_ID=mailrowob.selectedcandidateid.Selected_Candidate_ID).update(
                        BGVStatus="In Process"
                    )

                if(mailrowob.mailcategory=="Medical Test"):
                    #send mail code
                    Medicalmailto =[]
                    Medicalmail=DepartmentInformation.objects.filter(Department="Medical").first().Email
                    canname = selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName
                    subject = 'Candidate '+canname+' medical & drug test request'                    
                    canemail=selectedcandidateob.candidate.Email
                    if Medicalmail is not None:
                        Medicalmailto = Medicalmail.split(',')
                    # 'EmployeeID','Name','DoB','Age','Relation','Gender','Band','GMC coverage(INR)','GPA coverage(INR)','DOJ','Official MailID','Personal Email','Contact Number'

                    context = {
                        'canname': canname,
                        'canemail' : selectedcandidateob.candidate.Email,
                        'canphoneno' : personalinfoob.ContactNumber,
                        
                    }
                    body = EmailUtils.getEmailBody('Medical_Test_Mail.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("Medicalmail--"+Medicalmail)
                    print("Medicalmailto--"+str(Medicalmailto))
                    print("HRemail--"+emails.HREmail)
                    EmailUtils.sendEmail(subject, body, Medicalmailto, [emails.HREmail])

                    mailrowob.mailsent=True
                    mailrowob.mailsentat=datetime.now()
                    mailrowob.mailssentto=Medicalmail
                    mailrowob.save()
                    Selected_Candidates.objects.filter(Selected_Candidate_ID=mailrowob.selectedcandidateid.Selected_Candidate_ID).update(
                        Medicalteststatus="In Process"
                    )

                if(mailrowob.mailcategory=="Account Creation"):
                    #send mail code
                    ushremailarr = []
                    HRmail = emails.HREmail
                    HMname = emails.HMname
                    HMmail = emails.HMemail
                    reportingmanagersamname=selectedcandidateob.Reportingmanager
                    repmanager=AdUsers.objects.filter(UserName=reportingmanagersamname).first()
                    managername=repmanager.LastName+", " +repmanager.FirstName
                    manageremail=repmanager.Email
                    tomail1 = DepartmentInformation.objects.filter(Department="US HR").first().Email
                    if tomail1 is not None:
                        ushremailarr = tomail1.split(',')
                    canname = selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName
                    subject = 'Candidate '+canname+' account creation request'   
                    locale.setlocale(locale.LC_ALL, 'en_US')                  
                    context = {
                        'Candidatename': canname,
                        'Canfirstname': selectedcandidateob.candidate.CanFirstName,
                        'Canlastname': selectedcandidateob.candidate.CanLastName,
                        'Gender': personalinfoob.Gender,
                        'Title':selectedcandidateob.designation.DesignationName,
                        'Managername': managername,
                        'Managermail': manageremail,
                        'Locality': personalinfoob.Address, 
                        'startdate': (selectedcandidateob.DateOfJoining).strftime('%m/%d/%Y'),                        
                        'AvgBillRate': locale.currency(selectedcandidateob.candidate.AvgBillRate, grouping=True) ,
                        'joblocation': selectedcandidateob.candidate.Location.LocationName,
                        'emptype': selectedcandidateob.candidate.EmploymentType,
                        'HBU': selectedcandidateob.candidate.Jobpost.BusinessUnit.BusinessUnitName,
                        'GroupSupporting': selectedcandidateob.candidate.Jobpost.ServiceLine.ServiceLineName,
                        
                    }
                    body = EmailUtils.getEmailBody('Account_Creation_template.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("US HR--"+tomail1)
                    print("US HR Array--"+str(ushremailarr))
                    print("HRemail--"+emails.HREmail)
                    EmailUtils.sendEmail(subject, body, ushremailarr, [HRmail])

                    mailrowob.mailsent=True
                    mailrowob.mailsentat=datetime.now()
                    mailrowob.mailssentto=tomail1
                    mailrowob.save()

                if(mailrowob.mailcategory=="IT"):
                    #send mail code
                    ITemailarr = []
                    ITemail = DepartmentInformation.objects.filter(Department="IT").first().Email
                    # Adminemail = DepartmentInformation.objects.filter(Department="Admin").first().Email
                    canemployeeId = selectedcandidateob.EmployeeID 
                    canHRCid = selectedcandidateid.HRCID
                    canofficialmailId=selectedcandidateob.OfficialMailId
                    canphnNumber=personalinfoob.ContactNumber
                    if ITemail is not None:
                        ITemailarr = ITemail.split(',')
                    canname = selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName
                    subject = 'Candidate '+canname+' laptop arrange request'   
                    context = {
                        'CanName': canname,
                        'CanEmail': canofficialmailId,
                        'CanEmployeeID':canemployeeId,
                        'CanHRCID':canHRCid,
                        'CanContactNumber':canphnNumber,
                        'startdate': (selectedcandidateob.DateOfJoining).strftime('%m/%d/%Y'),
                        'canofficialmailId':canofficialmailId
                    }
                    body = EmailUtils.getEmailBody('IT_template.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("ITemail--"+ITemail)
                    print("ITemailarr--"+str(ITemailarr))
                    print("canofficialmailId--"+canofficialmailId)
                    print("HREmail--"+emails.HREmail)
                
                    EmailUtils.sendEmail(subject, body, ITemailarr, [emails.HREmail,canofficialmailId])

                    mailrowob.mailsent=True
                    mailrowob.mailsentat=datetime.now()
                    mailrowob.mailssentto=ITemail
                    mailrowob.save()
                if(mailrowob.mailcategory=="Admin"):
                    #send mail code
                    Adminemailarr =[]
                    Adminemail = DepartmentInformation.objects.filter(Department="Admin").first().Email
                    canemployeeId = selectedcandidateob.EmployeeID 
                    canHRCid = selectedcandidateid.HRCID
                    canofficialmailId=selectedcandidateob.OfficialMailId
                    canphnNumber=personalinfoob.ContactNumber
                    if Adminemail is not None:
                        Adminemailarr = Adminemail.split(',')
                    canname = selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName
                    subject = 'Candidate '+canname+' welcome kit request'   
                    context = {
                        'CanName': canname,
                        'CanEmail': canofficialmailId,
                        'CanEmployeeID':canemployeeId,
                        'CanHRCID':canHRCid,
                        'CanContactNumber':canphnNumber,
                        'startdate': (selectedcandidateob.DateOfJoining).strftime('%m/%d/%Y'),
                        'canofficialmailId':canofficialmailId
                    }
                    body = EmailUtils.getEmailBody('Admin_template.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("Adminemail--"+Adminemail)
                    print("Adminemailarr--"+str(Adminemailarr))
                    print("canofficialmailId--"+canofficialmailId)
                    print("HREmail--"+emails.HREmail)
                
                    EmailUtils.sendEmail(subject, body, Adminemailarr, [emails.HREmail,canofficialmailId])

                    mailrowob.mailsent=True
                    mailrowob.mailsentat=datetime.now()
                    mailrowob.mailssentto=Adminemail
                    mailrowob.save()

                 
                if(mailrowob.mailcategory=="Insurance"):
                    Insuranceemailarr = []
                    insuranceob=Insurance.objects.filter(BandId=selectedcandidateob.band.BandId).first()
                    
                    tomail = DepartmentInformation.objects.filter(Department="Insurance").first().Email
                    canemployeeid = selectedcandidateob.EmployeeID
                    canbandname=Band.objects.filter(BandId=selectedcandidateob.band.BandId).first().BandName
                    cangmccoverage=insuranceob.InsuranceLimit
                    cangpacoverage=insuranceob.AccidentLimit
                    candoj=selectedcandidateob.DateOfJoining.strftime('%d-%m-%Y')
                    canofficialmailid=selectedcandidateob.OfficialMailId
                    canpersonalemail=personalinfoob.Email
                    cancontactnumber=personalinfoob.ContactNumber
                    
                    row=[]
                    # for i in insurancedetailsob:
                    #     if i.Relationship!="Self":
                    #         row.append({'Name':i.Name,'DoB':i.DateOfBirth.strftime('%d-%m-%Y'),'Age':i.Age,'Relation':i.Relationship,'Gender':i.Gender})

                    HRmail = emails.HREmail
                    if tomail is not None:
                        Insuranceemailarr = tomail.split(',')
                    canname = selectedcandidateob.candidate.CanLastName +", "+ selectedcandidateob.candidate.CanFirstName
                    subject = 'Employee '+canname+' insurance initiation request from Belcan India'   
                    # 'EmployeeID','Name','DoB','Age','Relation','Gender','Band','GMC coverage(INR)','GPA coverage(INR)','DOJ','Official MailID','Personal Email','Contact Number'

                    context = {
                        'EmployeeID': canemployeeid,
                        'Candidatename': personalinfoob.Name,#aadhar full name from personal details
                        'canfirstName': selectedcandidateob.candidate.CanFirstName,#firstname 
                        'canlastName':  selectedcandidateob.candidate.CanLastName,#lastname 
                        'Band':canbandname,
                        'GMCcoverage':cangmccoverage,
                        'GPAcoverage':cangpacoverage,
                        'DOJ':candoj,
                        'OfficialMailID':canofficialmailid,
                        'PersonalMailID':canpersonalemail,
                        'ContactNumber':cancontactnumber,
                      
                    }
                    body = EmailUtils.getEmailBody('Can_Insurance_Details_template.html', context)
                    print("body--"+body)
                    print("subject--"+subject)
                    print("insuranceemail--"+tomail)
                    print("Insuranceemailarr--"+str(Insuranceemailarr))
                    print("HRmail--"+HRmail)
                    EmailUtils.sendEmail(subject, body, Insuranceemailarr, [HRmail])

                    mailrowob.mailsent=True
                    mailrowob.mailsentat=datetime.now()
                    mailrowob.mailssentto=tomail
                    mailrowob.save()
                mailsobj=Operationalmails.objects.filter(selectedcandidateid=selectedcandidateid)
                mailsserializer =operationalMailsSerializer(mailsobj,many=True)
                # logger.info({"res":"Email has been sent succesfully","data":mailsserializer.data})
                return Response({"res":"Email has been sent succesfully","data":mailsserializer.data},status=status.HTTP_200_OK)
                # return Response("Email has been sent succesfully",status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception while sending email : "+str(e))
            logger.error(traceback.format_exc())
            return Response("Exception while sending email : "+str(e),status=status.HTTP_400_BAD_REQUEST)

# class table(TemplateView):
#       template_name = 'Can_Insurance_Details_template.html'
      
#       def get_context_data(self, **kwargs):
#             ids = super(table,self).get_context_data(**kwargs)
#             ids['header'] = ['#', 'EmployeeID','Name','DoB','Age','Relation','Gender','Band','GMC coverage(INR)','GPA coverage(INR)','DOJ','Official MailID','Personal Email','Contact Number']
#             ids['rows'] = [{'EmployeeID':1,'Name':insuranceob.Name,'DoB':CandidateInsuranceDetails.DateOfBirth,'Age':CandidateInsuranceDetails.Age,'Relation':CandidateInsuranceDetails.Relationship,'Gender':CandidateInsuranceDetails.Gender},
#                            ]
#             return ids