
import decimal
import io
import os
import traceback
from HRproj.util.Mail.HR_Workflow_Emails import EmailUtils
from ManageInsurance.models import Insurance
from candidate.models.selected_Candidates_Model import Selected_Candidates
from HRproj.util.Constants.HR_WorkFlow_Constants import Constants1
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from candidate.models.candidatemodel import Candidate
from candidate.models.selected_Candidates_Model import  Selected_Candidates
from jobpost.models.jobpostapprovalmodel import JobPostApproval
from candidate.serializers import selectedcandidatesgridviewSerializer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from ManageBand.models import Band
from ManageSubBand.models import SubBand
from ManageDesignation.models import Designation
from datetime import datetime
from docxtpl import DocxTemplate
from django.core.files.uploadedfile import SimpleUploadedFile
from HRproj.settings import MEDIA_ROOT
from docx2pdf import convert
import random
import string
from django.contrib.auth.models import Group, User
from django.conf import settings
import locale
from jobpost.models.jobpoststakeholders import JobPostStakeHolders
from operationalmails.models import Operationalmails
from django.db import transaction
import logging
logger = logging.getLogger(__name__)
class updateselectedcandidate(ModelViewSet):


    @action(detail=True, methods=['post'])
    def updateselinterncandidate(self, request, format=None):
        logger.info("selected intern update starts")
        try:
            with transaction.atomic():
                selectedcandidate =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])
                designation= Designation.objects.get(DesignationId=request.data['designation'])
                startdate=request.data["StartDate"]            
                salary=request.data["FinalCTC"]             
                duration = request.data["Duration"]  
                
            
                sco =  Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(
                    designation= designation,      
                    DateOfJoining=startdate,
                    FinalCTC = salary,
                    Duration = duration,                
                    Modified_By=request.data["Modified_By"],
                    Modified_On=datetime.now(),

                )
                # create offer letter from template

                buffer = io.BytesIO()
                doc = DocxTemplate("Belcan_India_Internship_Template.docx")
                context = self.getInternContext(selectedcandidate, designation, startdate,
                                        salary, duration)
                doc.render(context)
                doc.save(buffer)
                buffer.seek(0)                
                content_file = SimpleUploadedFile(selectedcandidate.candidate.CanLastName+'_'+selectedcandidate.candidate.CanFirstName+'_Internship Letter.docx', buffer.getvalue())
                print(type(content_file))
                sco =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])

                if sco.OfferLetter.__bool__()  and os.path.exists(os.path.join(MEDIA_ROOT, str(sco.OfferLetter))):
                    os.remove(os.path.join(MEDIA_ROOT, str(sco.OfferLetter)))

                sco.OfferLetter= content_file
                sco.OfferLetterSent = False
                sco.save()
                # covert document to PDF 
                convert(os.path.join(MEDIA_ROOT, str(sco.OfferLetter))) 


                # insert or update record in Operationalmails
                # self.insertorupdateoperationalmails(request.data["selectedcandidateid"])


                logger.info("Internship letter generated successfully")
                return  Response("Internship Letter generated successfully",status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception while generation internship letter "+str(e))
            logger.error(traceback.format_exc())
            return  Response("Exception while generation internship letter "+str(e),status=status.HTTP_400_BAD_REQUEST)        
        finally:
            logger.info("selected intern update ends")

    @action(detail=True, methods=['post'])
    def updateselcontractcandidate(self, request, format=None):
        logger.info("selected contract candidate update starts")
        try:
            with transaction.atomic():
                selectedcandidate =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])
                designation= Designation.objects.get(DesignationId=request.data['designation'])
                startdate=request.data["StartDate"]
                enddate=request.data["EndDate"]
                salary=request.data["FinalCTC"]
                hourspermonth = request.data["NoOfHours"]  
                duration = request.data["Duration"]  
                Responsibilities=request.data["Responsibilities"]
                
            
                sco =  Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(

                    designation= designation,      
                    DateOfJoining=startdate,
                    FinalCTC = salary,
                    EndDate = enddate,
                    NoOfHours = hourspermonth,
                    Duration = duration,                
                    Responsibilities=Responsibilities,
                    Modified_By=request.data["Modified_By"],
                    Modified_On=datetime.now(),

                )
                # create offer letter from template

                buffer = io.BytesIO()
                doc = DocxTemplate("Belcan_India_Contract_Agreement_Template.docx")
                context = self.getContractContext(selectedcandidate, designation, startdate,
                                        enddate, salary,hourspermonth, duration, Responsibilities)
                doc.render(context)
                doc.save(buffer)
                buffer.seek(0)
                content_file = SimpleUploadedFile(selectedcandidate.candidate.CanLastName+'_'+selectedcandidate.candidate.CanFirstName+'_Contract Agreement.docx', buffer.getvalue())
                print(type(content_file))
                sco =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])

                if sco.OfferLetter.__bool__()  and os.path.exists(os.path.join(MEDIA_ROOT, str(sco.OfferLetter))):
                    os.remove(os.path.join(MEDIA_ROOT, str(sco.OfferLetter)))

                sco.OfferLetter= content_file
                sco.OfferLetterSent = False
                sco.save()
                # covert document to PDF 
                convert(os.path.join(MEDIA_ROOT, str(sco.OfferLetter))) 

                # insert or update record in Operationalmails
                # self.insertorupdateoperationalmails(request.data["selectedcandidateid"])           
                logger.info("Contract Agreement generated sucessfully")
                return  Response("Contract Agreement generated sucessfully",status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception while generating Contract Agreement "+str(e))
            logger.error(traceback.format_exc())
            return  Response("Exception while generating Contract Agreement "+str(e),status=status.HTTP_400_BAD_REQUEST)        
        finally:
            logger.info("selected contract candidate update ends")

    @action(detail=True, methods=['post'])
    def updateselcandidate(self, request, format=None):
        logger.info("selected candidate update starts")
        try:
            with transaction.atomic():
                selectedcandidate =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])
                designation= Designation.objects.get(DesignationId=request.data['designation'])
                band=Band.objects.get(BandId=request.data['band'])
                # subband=SubBand.objects.get(SubBandId=request.data['subband'])
                try:
                    subband=SubBand.objects.get(SubBandId=request.data['subband'])
                except:
                    subband=None                
                DateOfJoining=request.data["doj"]
                FinalCTC=request.data["FinalCTC"]  
                
                ShiftAllowance = request.data["ShiftAllowance"] if request.data["ShiftAllowance"] is not None else 0         
                Isvariable = request.data["IsVariable"]
                VariablePerc = request.data["VariablePerc"]
                # VariablePay = request.data["VariablePay"]
                MQVariable=request.data["MQVariable"]
                Is_Eligible_annu_Mgnt_Bonus=request.data["Is_Eligible_annu_Mgnt_Bonus"]
                Is_Eligible_Joining_Bonus=request.data["Is_Eligible_Joining_Bonus"]  
                JoiningBonus = request.data["JoiningBonus"]            
                IS_Eligible_Monthly_Incentive=request.data["IS_Eligible_Monthly_Incentive"]          
                if Isvariable is True:       
                    VariablePay = round((FinalCTC * VariablePerc)/(100))   
                    FixedCTC = FinalCTC-VariablePay

                elif Isvariable is False:
                    FixedCTC =  FinalCTC  
                    VariablePay = 0 
                sco =  Selected_Candidates.objects.filter(Selected_Candidate_ID=request.data["selectedcandidateid"]).update(
                    designation= designation,
                    band=band,
                    subband=subband,
                    DateOfJoining=DateOfJoining,
                    FixedCTC=FixedCTC,
                    IsVariable = Isvariable,
                    VariablePerc = VariablePerc,
                    VariablePay=VariablePay,
                    FinalCTC = FinalCTC,
                    ShiftAllowance = ShiftAllowance,
                    MQVariable=MQVariable,
                    Is_Eligible_annu_Mgnt_Bonus=Is_Eligible_annu_Mgnt_Bonus,
                    Is_Eligible_Joining_Bonus=Is_Eligible_Joining_Bonus,
                    JoiningBonus = JoiningBonus,
                    IS_Eligible_Monthly_Incentive=IS_Eligible_Monthly_Incentive,
                    Modified_By=request.data["Modified_By"],
                    Modified_On=datetime.now(),

                )
                # create offer letter from template

                buffer = io.BytesIO() 
                if Isvariable is True:
                    doc = DocxTemplate("Belcan_India_Offer_Letter_Variable_Pay_Template.docx")
                else:    
                    doc = DocxTemplate("Belcan_India_Offer_Letter_Template.docx")
                context = self.getContext(selectedcandidate, designation, band, subband, DateOfJoining,
                                        FinalCTC, ShiftAllowance,Isvariable, VariablePerc, MQVariable, Is_Eligible_annu_Mgnt_Bonus,
                                        Is_Eligible_Joining_Bonus, IS_Eligible_Monthly_Incentive)
                doc.render(context)
                doc.save(buffer)
                buffer.seek(0)
                # print(buffer.getvalue())
                content_file = SimpleUploadedFile(selectedcandidate.candidate.CanLastName+'_'+selectedcandidate.candidate.CanFirstName+'_OfferLetter.docx', buffer.getvalue())
                sco =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])

                if sco.OfferLetter.__bool__()  and os.path.exists(os.path.join(MEDIA_ROOT, str(sco.OfferLetter))):
                    os.remove(os.path.join(MEDIA_ROOT, str(sco.OfferLetter)))

    

                sco.OfferLetter= content_file
                sco.OfferLetterSent = False
                sco.save()

                # covert document to PDF 
                convert(os.path.join(MEDIA_ROOT, str(sco.OfferLetter))) 


                if Is_Eligible_Joining_Bonus is True:
                    buffer1 = io.BytesIO()    
                    doc1 = DocxTemplate("Belcan_Joining_Bonus_Template.docx")
                    context1 = self.getJoiningBonusContext(selectedcandidate, designation, band, subband, JoiningBonus)
                    doc1.render(context1)
                    doc1.save(buffer1)
                    buffer1.seek(0)
                    content_file1 = SimpleUploadedFile(selectedcandidate.candidate.CanLastName+'_'+selectedcandidate.candidate.CanFirstName+'_JoiningBonusLetter.docx', buffer1.getvalue())
                    # sco1 =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])

                    if sco.JoiningBonusLetter.__bool__()  and os.path.exists(os.path.join(MEDIA_ROOT, str(sco.JoiningBonusLetter))):
                        os.remove(os.path.join(MEDIA_ROOT, str(sco.JoiningBonusLetter)))

                    sco.JoiningBonusLetter= content_file1
                    sco.save()    
                    # covert document to PDF    
                    convert(os.path.join(MEDIA_ROOT, str(sco.JoiningBonusLetter)))          

                else:
                    
                    if sco.JoiningBonusLetter.__bool__():
                        strpdf = str(sco.OfferLetter).replace(".docx", ".pdf")
                        if os.path.exists(os.path.join(MEDIA_ROOT, strpdf)):
                            os.remove(os.path.join(MEDIA_ROOT, strpdf))  

                    sco =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])

                    if sco.JoiningBonusLetter.__bool__()  and os.path.exists(os.path.join(MEDIA_ROOT, str(sco.JoiningBonusLetter))):
                        os.remove(os.path.join(MEDIA_ROOT, str(sco.JoiningBonusLetter)))

                    sco.JoiningBonusLetter= None
                    sco.save()  

    
                
                # insert or update record in Operationalmails
                # self.insertorupdateoperationalmails(request.data["selectedcandidateid"])             
                logger.info("Documents generated successfully")
                return  Response("Documents generated successfully",status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception while generating documents "+str(e))
            logger.error(traceback.format_exc())
            return Response("Exception while generating documents "+str(e),status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def sendOfferLetter(self, request, format=None):
        try:
            with transaction.atomic():
                joiningbonuspdfpath = None
                selectedcandidate =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])
                if selectedcandidate is not None:
                    # create user and assign candidate role 
                    canlastname = selectedcandidate.candidate.CanLastName
                    canfirstname = selectedcandidate.candidate.CanFirstName
                    canemail = selectedcandidate.candidate.Email
                    dateofjoin = selectedcandidate.DateOfJoining

            
                    suff1 = self.suffix1(dateofjoin.day)
                    dateofjoining = dateofjoin.strftime("%B")+" "+dateofjoin.strftime("%d")+suff1+","+dateofjoin.strftime("%Y")

                    # dateofjoining = dateofjoin.strftime("%B %d" + self.suffix1(dateofjoin.day)+",%Y")
                    # dateofjoining = dateofjoin.strftime("%B")+" "+dateofjoin.strftime("%d")+
                    user1 = User.objects.filter(first_name=canfirstname, last_name=canlastname, email=canemail).first()
                    if user1 is None:
                        username = canfirstname[0:1]+canlastname+str(selectedcandidate.Selected_Candidate_ID)
                        password = self.get_random_password()
                        user = User.objects.create_user(username, canemail, password)
                        user.first_name = canfirstname
                        user.last_name = canlastname  
                        user.save()
                        g = Group.objects.get(name = 'Candidate')
                        g.user_set.add(user)
                    else:
                        username =  user1.username
                        password = self.get_random_password() 
                        user1.set_password(password)
                        user1.save()  
    
                    # Convert Offerletter doc to PDF
                    # if os.path.exists(os.path.join(MEDIA_ROOT, str(selectedcandidate.OfferLetter))):
                    #     convert(os.path.join(MEDIA_ROOT, str(selectedcandidate.OfferLetter)))
                    docpath = os.path.join(MEDIA_ROOT, str(selectedcandidate.OfferLetter)) 
                    pdfpath = docpath.replace(".docx", ".pdf")


                    if selectedcandidate.JoiningBonusLetter.__bool__()  and os.path.exists(os.path.join(MEDIA_ROOT, str(selectedcandidate.JoiningBonusLetter))):
                        joiningbonusdocpath = os.path.join(MEDIA_ROOT, str(selectedcandidate.JoiningBonusLetter))
                        joiningbonuspdfpath = joiningbonusdocpath.replace(".docx", ".pdf")
                    # with open(pdfpath, 'r') as f:
                        # file = f

                    # send email to candidate with offerletter attachment.
                    emails = JobPostStakeHolders.objects.filter(JobPostId=selectedcandidate.candidate.Jobpost.JobPostId).first()
                    subject = 'Belcan India Offer Letter-'+canfirstname+" "+canlastname
                    print('candidatename--'+canfirstname+" "+canlastname)
                    print('url--'+settings.APP_URL)
                    print('dateofjoining--'+dateofjoining)
                    print('username--'+username)
                    print('password--'+password)
                    context = {
                        'candidatename': canfirstname+" "+canlastname,                    
                        'url' : settings.APP_URL,
                        'dateofjoining' : dateofjoining,
                        'username' : username,
                        'password' : password
                    }
                    body = EmailUtils.getEmailBody('Can_Offer_letter_template.html', context)
                    print('body--'+body)
                    print('subject--'+subject)
                    print('canemail--'+canemail)
                    print('HRemail--'+emails.HREmail)
                    print('recruiteremail--'+emails.RecruiterEmail)
                    # print(canemail)
                    # print(jobpost1.Email)                 
                    EmailUtils.sendEmailWithAttachments(subject, body, [canemail], None,[emails.HREmail, emails.RecruiterEmail], pdfpath, joiningbonuspdfpath)    
                    # update OfferLetterSent to True
                    selectedcandidate.username = username
                    selectedcandidate.OfferLetterSent = True
                    selectedcandidate.save()
                logger.info("Documents has been sent succesfully")
                return  Response("Documents has been sent succesfully",status=status.HTTP_200_OK)     

        except Exception as ex:
            logger.error("Exception while sending the offerletter "+str(ex))
            logger.error(traceback.format_exc())
            return  Response("Exception while sending the offerletter "+str(ex),status=status.HTTP_400_BAD_REQUEST)  
    
    @action(detail=True, methods=['post'])
    def getAnnexureDetails(self, request, format=None):
        try:
            selectedcandidate =  Selected_Candidates.objects.get(Selected_Candidate_ID=request.data["selectedcandidateid"])
            designation= Designation.objects.get(DesignationId=request.data['designation'])
            band=Band.objects.get(BandId=request.data['band'])
            # subband=SubBand.objects.get(SubBandId=request.data['subband'])
            try:
                subband=SubBand.objects.get(SubBandId=request.data['subband'])
            except:
                subband=None              
            DateOfJoining=request.data["doj"]
            # FixedCTC=request.data["FixedCTC"]
            FinalCTC=request.data["FinalCTC"]  
             
            ShiftAllowance = request.data["ShiftAllowance"] if request.data["ShiftAllowance"] is not None else 0         
            Isvariable = request.data["IsVariable"]
            VariablePerc = request.data["VariablePerc"]
            # VariablePay = request.data["VariablePay"]
            MQVariable=request.data["MQVariable"]
            Is_Eligible_annu_Mgnt_Bonus=request.data["Is_Eligible_annu_Mgnt_Bonus"]
            Is_Eligible_Joining_Bonus=request.data["Is_Eligible_Joining_Bonus"]  
            JoiningBonus = request.data["JoiningBonus"]            
            IS_Eligible_Monthly_Incentive=request.data["IS_Eligible_Monthly_Incentive"]
            context = self.getContext(selectedcandidate, designation, band, subband, DateOfJoining,
                                    FinalCTC, ShiftAllowance,Isvariable, VariablePerc, MQVariable, Is_Eligible_annu_Mgnt_Bonus,
                                    Is_Eligible_Joining_Bonus, IS_Eligible_Monthly_Incentive)
            # logger.info(context)
            return Response(context,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception while getting annexure details "+str(e))
            logger.error(traceback.format_exc())
            return Response("Exception while getting annexure details "+str(e),status=status.HTTP_400_BAD_REQUEST)

    def getJoiningBonusContext(self,selectedcandidate, designation, band, subband, JoiningBonus):
      
        varDesignation = None
        varName =  None
        varBand = None
        varSubBand = None
        varJB = None
        varJBWords = None
              
 

        if designation is not None:
            varDesignation = designation.DesignationName
        if selectedcandidate is not None: 
            varName =  selectedcandidate.candidate.CanLastName+' '+selectedcandidate.candidate.CanFirstName
        if  band is not None:
            varBand = band.BandName    
        if  subband is not None:
            varSubBand = subband.SubBandName
        varJB = locale.format("%.0f", JoiningBonus, grouping=True)  
        varJBWords = self.num2words(JoiningBonus)

        context = {                  
                    "varName"  : varName,
                    "varDesignation" : varDesignation,    
                    "varBand" : varBand,
                    "varSubBand" : varSubBand,      
                    "varJB" : varJB,
                    "varJBWords" : varJBWords
                    


                 }
        return context
    
    def getInternContext(self,selectedcandidate, designation, startdate, salary, 
                                   duration):
        varDate = None
        varDesignation = None
        varName =  None
        varLocation = None
        varStartDate = None
        varPeriod = None
        varStipend = None
              
        
        dt = datetime.now().date()
        suff = self.suffix1(dt.day)       
        varDate = dt.strftime("%B")+" "+dt.strftime("%d")+suff+", "+dt.strftime("%Y")

        startdate=datetime.strptime(startdate,'%Y-%m-%d')
        suff1 = self.suffix1(startdate.day)
        startdate = startdate.strftime("%d")+suff1+" "+startdate.strftime("%B")+" "+startdate.strftime("%Y")
        varStartDate = startdate      
        locale.setlocale(locale.LC_ALL, 'hi_IN')
        if designation is not None:
            varDesignation = designation.DesignationName
        if selectedcandidate is not None: 
            varName =  selectedcandidate.candidate.CanLastName+' '+selectedcandidate.candidate.CanFirstName
            varLocation = selectedcandidate.candidate.Location.LocationName
        varStipend = locale.format("%.0f", salary, grouping=True)  
        varPeriod =  duration  

        context = {
                    "varDate" :varDate,
                    "varName"  : varName,
                    "varDesignation" : varDesignation,    
                    "varLocation" : varLocation,
                    "varStartDate" : varStartDate,      
                    "varPeriod" : varPeriod,
                    "varStipend" : varStipend
                    


                 }
        return context    

    def getContractContext(self,selectedcandidate, designation, startdate, enddate, salary, 
                                  hourspermonth, duration, Responsibilities):
        varDate = None
        varDesignation = None
        varName =  None
        varLocation = None
        varStartDate = None
        varEndDate = None
        varHours  = None
        varPeriod = None
        varSalary = None
        varResponsibilities = None
              
        
        dt = datetime.now().date()
        suff = self.suffix1(dt.day)       
        varDate = dt.strftime("%B")+" "+dt.strftime("%d")+suff+", "+dt.strftime("%Y")

        startdate=datetime.strptime(startdate,'%Y-%m-%d')
        suff1 = self.suffix1(startdate.day)
        startdate = startdate.strftime("%d")+suff1+" "+startdate.strftime("%B")+" "+startdate.strftime("%Y")
        varStartDate = startdate

        enddate=datetime.strptime(enddate,'%Y-%m-%d')
        suff1 = self.suffix1(enddate.day)
        enddate = enddate.strftime("%d")+suff1+" "+enddate.strftime("%B")+" "+enddate.strftime("%Y")
        varEndDate = enddate        
        locale.setlocale(locale.LC_ALL, 'hi_IN')
        if designation is not None:
            varDesignation = designation.DesignationName
        if selectedcandidate is not None: 
            varName =  selectedcandidate.candidate.CanLastName+' '+selectedcandidate.candidate.CanFirstName
            varLocation = selectedcandidate.candidate.Location.LocationName
        varSalary = locale.format("%.0f", salary, grouping=True)  
        varHours =   hourspermonth
        varPeriod =  duration  
        varResponsibilities = Responsibilities

        context = {
                    "varDate" :varDate,
                    "varName"  : varName,
                    "varDesignation" : varDesignation,     
                    "varSalary" : varSalary,
                    "varLocation" : varLocation,
                    "varStartDate" : varStartDate,      
                    "varEndDate" : varEndDate,
                    "varHours" : varHours,
                    "varPeriod" : varPeriod,
                    "varResponsibilities" : varResponsibilities,


                 }
        return context         
    
    def getContext(self,selectedcandidate, designation, band, subband, DateOfJoining, 
                                  FinalCTC, ShiftAllowance,Isvariable, VariablePerc, MQVariable,                                                                             Is_Eligible_annu_Mgnt_Bonus,
                                  Is_Eligible_Joining_Bonus, IS_Eligible_Monthly_Incentive):
        
        varDOJ = None
        varDate = None
        varDesignation = None
        varName =  None
        varLocation = None
        varBand = None
        varSubBand = None 
        varGMI = None
        varGPA = None
        iSMngtBonus = False
        iSVariablePay = False
        iSJoinBonus = False
        iSMonthIncentive = False
        varSalary = None
        varSalaryWords = None
        varTotalACTC = None
        varABasic = None
        varMBasic = None
        varAHRA = None
        varMHRA = None
        varAPF = None
        varMPF = None
        iSBonus  = False
        varABonus = None
        varMBonus = None
        iSShiftAllow   = False
        varAShiftAllow = None
        varMShiftAllow = None
        varAFBP   = None
        varMFBP = None
        varTotalMCTC = None

        businessunitname = None
        varTotalFixedCTC = None
        varVariablePay = None
        varFixedPayPerc = None
        varVariablePayPerc = None
        varMQVariable = None


        dt = datetime.now().date()
        suff = self.suffix1(dt.day)
        # varDate = dt.strftime("%B %d"+day+", %Y")
        varDate = dt.strftime("%B")+" "+dt.strftime("%d")+suff+", "+dt.strftime("%Y")

        DateOfJoining=datetime.strptime(DateOfJoining,'%Y-%m-%d')
        suff1 = self.suffix1(DateOfJoining.day)
        DateOfJoining = DateOfJoining.strftime("%d")+suff1+" "+DateOfJoining.strftime("%B")+", "+DateOfJoining.strftime("%Y")
        # DateOfJoining=DateOfJoining.strftime("%d"+self.suffix1(DateOfJoining.day)+" %B, %Y")
        # # DateOfJoining = DateOfJoining.strftime("%B %d, %Y")
        varDOJ = DateOfJoining

        locale.setlocale(locale.LC_ALL, 'hi_IN')
        if designation is not None:
            varDesignation = designation.DesignationName
        if selectedcandidate is not None: 
            varName =  selectedcandidate.candidate.CanLastName+' '+selectedcandidate.candidate.CanFirstName
            varLocation = selectedcandidate.candidate.Jobpost.Location.LocationName
            businessunitname = selectedcandidate.candidate.Jobpost.BusinessUnit.BusinessUnitName
        
        if  band is not None:
            varBand = band.BandName
            insurance = Insurance.objects.filter(BandId = band.BandId).first()
            if insurance is not None: 
                
                varGMI = locale.format("%.0f", insurance.InsuranceLimit, grouping=True)
                varGPA = locale.format("%.0f", insurance.AccidentLimit, grouping=True)
    
        if  subband is not None:
            varSubBand = subband.SubBandName
        iSMngtBonus = Is_Eligible_annu_Mgnt_Bonus
        iSVariablePay = Isvariable
        iSJoinBonus = Is_Eligible_Joining_Bonus
        iSMonthIncentive = IS_Eligible_Monthly_Incentive 

        

        varTotalACTC = FinalCTC

        if Isvariable == True:
           varVariablePayPerc = VariablePerc
           varVariablePay = round((varTotalACTC * varVariablePayPerc)/100)
           varFixedPayPerc = 100-varVariablePayPerc
           varTotalFixedCTC = varTotalACTC-varVariablePay
           varTotalMCTC = round(varTotalFixedCTC/12)
           varMQVariable = MQVariable
           

        elif Isvariable == False:
            varTotalFixedCTC =  varTotalACTC           
            varTotalMCTC = round(varTotalACTC/12)

        if varTotalACTC is not None:
           varSalary = locale.format("%.0f", varTotalACTC, grouping=True)
           varSalaryWords = self.num2words(varTotalACTC)
           

        if varTotalFixedCTC is not None:  
           varABasic = round(varTotalFixedCTC * 0.4)
           varMBasic = round(varABasic/12)

        if varMBasic is not None and varMBasic < 15000:
            varMBasic = 15000
            varABasic = round(varMBasic * 12)
        if varABasic is not None:
            varAHRA = round(varABasic * 0.4)
            varMHRA = round(varAHRA/12)
            varAPF = round(varABasic * 0.12)
            varMPF = round(varAPF/12)
        if varMBasic is not None and varMBasic <= 21000:  
            iSBonus = True
            varMBonus = 1400
            varABonus = round(varMBonus * 12)

        if businessunitname is not None and businessunitname == "Workforce Solutions":
            iSShiftAllow = True
            varMShiftAllow = ShiftAllowance
            varAShiftAllow = round(varMShiftAllow * 12)
        if varTotalFixedCTC is not None and varABasic is not None and varAHRA is not None and varAPF is not None:
            
            varAFBP = round(varTotalFixedCTC-(varABasic+varAHRA+varAPF))
        if iSBonus is True:
            varAFBP =   round(varAFBP-varABonus)
        if iSShiftAllow is True:
             varAFBP = round(varAFBP- varAShiftAllow)
        if varAFBP is not None:
            varMFBP = round(varAFBP/12)


        context = {
                    "varDate" :varDate,
                    "varName"  : varName,
                    "varDesignation" : varDesignation,
                    "varBand" : varBand,
                    "varSubBand" : varSubBand,
                    "varDOJ" : varDOJ,
                    "varSalary" : varSalary,
                    "varSalaryWords" : varSalaryWords,
                    "varLocation" : varLocation,
                    "varTotalFixedCTC" : varTotalFixedCTC,      
                    "varTotalACTC" : varTotalACTC,
                    "varTotalMCTC" : varTotalMCTC,
                    "varABasic" : varABasic,
                    "varMBasic" : varMBasic,
                    "varAHRA" : varAHRA,
                    "varMHRA" : varMHRA,
                    "varAPF" : varAPF,
                    "varMPF" : varMPF,
                    "iSBonus" : iSBonus,
                    "varABonus" : varABonus,
                    "varMBonus" : varMBonus,
                    "iSShiftAllow" : iSShiftAllow ,
                    "varAShiftAllow" : varAShiftAllow,
                    "varMShiftAllow" : varMShiftAllow,
                    "varAFBP" : varAFBP,
                    "varMFBP" : varMFBP,
                    "varGMI" : varGMI,
                    "varGPA" : varGPA,
                    "iSMngtBonus" : iSMngtBonus,                    
                    "iSJoinBonus" : iSJoinBonus ,
                    "iSMonthIncentive" : iSMonthIncentive,
                    "iSVariablePay" : iSVariablePay,
                    "varVariablePay": varVariablePay,
                    "varFixedPayPerc" : varFixedPayPerc,
                    "varVariablePayPerc" :varVariablePayPerc,
                    "varMQVariable" : varMQVariable


                 }
        return context 

    def num2words(self,num):
        num = decimal.Decimal(num)
        decimal_part = num - int(num)
        num = int(num)

        if decimal_part:
            return self.num2words(num) + " point " + (" ".join(self.num2words(i) for i in str(decimal_part)[2:]))

        under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

        if num < 20:
            return under_20[num]

        if num < 100:
            return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

        # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
        pivot = max([key for key in above_100.keys() if key <= num])

        return self.num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot==0 else ' ' + self.num2words(num % pivot))
    def get_random_password(self):
        random_source = string.ascii_letters + string.digits
        # select 1 lowercase
        password = random.choice(string.ascii_lowercase)
        # select 1 uppercase
        password += random.choice(string.ascii_uppercase)
        # select 1 digit
        password += random.choice(string.digits)
        # select 1 special symbol
        # password += random.choice(string.punctuation)

        # generate other characters
        for i in range(6):
            password += random.choice(random_source)

        password_list = list(password)
        # shuffle all characters
        random.SystemRandom().shuffle(password_list)
        password = ''.join(password_list)
        return password
    
    def suffix1(self,day):
        suffix = ""
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        if (suffix != ""):
            suffix =self.get_super(suffix)    
        return suffix

    def get_super(self,x):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
        res = x.maketrans(''.join(normal), ''.join(super_s))
        return x.translate(res)  

    # def insertorupdateoperationalmails(self, selectedcandidateid):
    #     offermailcount = Operationalmails.objects.filter( selectedcandidateid=selectedcandidateid, mailcategory="Offer Letter" ).__len__()
    #     if offermailcount == 0:
    #         Operationalmails.objects.create(
    #             selectedcandidateid=selectedcandidateid,
    #             mailcategory="Offer Letter",
    #             mailsent=False,
    #             mailsentat=None,
    #             mailssentto=None
    #         )           
    #     else:
    #         Operationalmails.objects.filter( selectedcandidateid=selectedcandidateid, mailcategory="Offer Letter" ).update(
    #             mailsent=False,
    #             mailsentat=None,
    #             mailssentto=None
    #         )