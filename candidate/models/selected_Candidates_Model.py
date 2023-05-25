import os
from django.db import models
from candidate.models.Feedback_Category_Model import Feedback_Category
from candidate.models.candidatemodel import Candidate
from ManageBand.models import Band
from ManageSubBand.models import SubBand
from candidate.models.CandidatecategoryModel import candidatecategorymodel
from ManageDesignation.models import Designation
class Selected_Candidates(models.Model):
    def get_upload_path(instance, filename):
        return os.path.join(str(instance.candidate.Jobpost.JobCode),str(instance.candidate.CandidateCode), 'OfferLetter',filename)
    def get_upload_path1(instance, filename):
        return os.path.join(str(instance.candidate.Jobpost.JobCode),str(instance.candidate.CandidateCode), 'JoiningBonusLetter',filename)        
    Selected_Candidate_ID=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(Candidate,null=True,on_delete=models.DO_NOTHING,db_column="Candidate_ID")
    IsOfferAccepted=models.BooleanField(null=False,default=False,db_column="Is_Offer_Accepted")
    IsJoined=models.BooleanField(null=False,default=False,db_column="Is_Joined")
    HRCID=models.CharField(max_length=100,null=True,default=None,db_column="HRC_ID")
    EmployeeID=models.CharField(max_length=100,null=True,default=None,db_column="Employee_ID")  
    designation=models.ForeignKey(Designation,on_delete=models.DO_NOTHING,null=True,default=None,db_column="Designation_ID")
    subband=models.ForeignKey(SubBand,null=True,on_delete=models.DO_NOTHING,default=None,db_column="SubBandId")
    band=models.ForeignKey(Band,null=True,on_delete=models.DO_NOTHING,default=None,db_column="BandId")
    DateOfJoining=models.DateField(null=True,default=None,db_column="Date_Of_Joining")
    FixedCTC=models.FloatField(db_column="Fixed_CTC",null=False,default=0)
    IsVariable=models.BooleanField(null=True,default=None,db_column="Is_Variable")
    VariablePerc=models.FloatField(null=True,default=0,db_column="Variable_Perc")
    VariablePay=models.FloatField(null=True,default=0,db_column="Variable_Pay")
    MQVariable=models.CharField(null=True,default=None,max_length=20)
    FinalCTC=models.FloatField(db_column="Final_CTC",null=False,default=0)
    ShiftAllowance = models.FloatField(db_column="Shift_Allowance",default=None, null=True)
    # candidatecategory=models.ForeignKey(candidatecategorymodel,null=True,on_delete=models.DO_NOTHING,db_column="candidate_category_ID")
    Is_Eligible_annu_Mgnt_Bonus=models.BooleanField(default=False,null=False,db_column="IsEligibleannuMgntBonus")
    Is_Eligible_Joining_Bonus=models.BooleanField(default=False,null=False,db_column="IsEligibleJoiningBonus")
    JoiningBonus = models.FloatField(default=None,db_column="Joining_Bonus",null=True)
    IS_Eligible_Monthly_Incentive=models.BooleanField(default=False,null=False,db_column="ISEligibleMonthlyIncentive")
    OfferLetter = models.FileField(upload_to=get_upload_path,null=True,default=None,db_column="Offer_Letter")
    Created_By=models.CharField(max_length=50,null=True,default=None,db_column="CreatedBy")
    Created_on=models.DateField(db_column="Createdon",default=None,null=True)
    Modified_By=models.CharField(max_length=50,null=True,default=None,db_column="ModifiedBy")
    Modified_On=models.DateField(db_column="ModifiedOn",default=None,null=True)
    VerificationStatus = models.CharField(max_length=20,null=True,default=None,db_column="Verification_Status")
    VerificationComments = models.CharField(max_length=500,null=True,default=None,db_column="Verification_Comments")
    BGVStatus = models.CharField(max_length=20,null=True,default=None,db_column="BGV_Status")
    Medicalteststatus = models.CharField(max_length=20,null=True,default=None,db_column="Medical_Test_Status")
    OfficialMailId = models.CharField(max_length=100,null=True,default=None,db_column="OfficialMailId")
    EndDate=models.DateTimeField(db_column='EndDate', default=None,null =True, blank=True)
    NoOfHours=models.IntegerField(null=True, default=None)
    Duration = models.IntegerField(null=True, default=None,db_column='Duration')
    JoiningBonusLetter = models.FileField(upload_to=get_upload_path1,null=True,default=None,db_column="JoiningBonus_Letter")
    Responsibilities=models.CharField(max_length=2000,null=True,default=None,db_column="Responsibilities")
    Brief_Description=models.CharField(max_length=500,null=True,default=None,db_column="Brief_Description")
    OfferLetterSent=models.BooleanField(null=True,default=False, db_column="OfferLetter_Sent")
    Reportingmanager=models.CharField(max_length=50,null=True,default=None,db_column="Reporting_Manager")
    username=models.CharField(max_length=50,null=True,default=None,db_column="User_Name")
    class Meta:  
        db_table="Selected_Candidates"