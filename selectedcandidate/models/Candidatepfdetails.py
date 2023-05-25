from django.db import models
from candidate.models.candidatemodel import Candidate
from candidate.models.selected_Candidates_Model import Selected_Candidates
from selectedcandidate.models.Candidatebankdetails import CandidateBankDetails
from selectedcandidate.models.Candidatedducationaldetails import CandidateEducationalDetails
from selectedcandidate.models.Candidatepersonalinfo import CandidatePersonalInfo

class CandidatePfDetails(models.Model):
    Id = models.AutoField(primary_key=True,db_column='ID')
    selectedcandidateid=models.ForeignKey(Selected_Candidates,null=True,on_delete=models.DO_NOTHING,db_column="Selected_Candidate_ID")
    PreviousCompanyUAN = models.CharField(null=True, max_length=50, db_column='Prev_Company_UAN')
    PreviousMemberId = models.CharField(null=True, max_length=50, db_column='Prev_Mem_ID')
    MemberNameAsPerAadhar = models.CharField(null=True, max_length=100, db_column='Member_Name_As_Per_Aadhar')
    AADHAR = models.CharField(null =True, max_length=20, db_column='AADHAR')
    DateOfBirth = models.CharField(null =True, max_length=20, db_column='DateOfBirth')
    Date_Of_Joining = models.CharField(null =True, max_length=20, db_column='Date_Of_Joining')
    Gender = models.CharField(null =True, max_length=20, db_column='Gender')
    FatherOrHusbandName = models.CharField(null = True, max_length=100, db_column='FatherOrHusbandName')
    Relation = models.CharField(null=True, max_length=50, db_column='Relation')
    Marital_status = models.CharField(null =True, max_length=20, db_column='Marital_status')
    InternationalWorker = models.BooleanField(null =True,default=False, db_column='International_Worker')
    ContactNumber = models.CharField(null =True, max_length=20, db_column='ContactNumber')
    Email =  models.CharField(null =True, max_length=50,db_column='Email')
    Nationality = models.CharField(null=True, max_length=100, db_column='Nationality')
    wages = models.CharField(null=True, default=None, max_length=50, db_column='Wages')
    Qualification = models.CharField(null =True, max_length=50, db_column='Qualification')
    CountryOfOrigin = models.CharField(null=True, max_length=100, db_column='Country_Of_Origin')
    PassportNumber = models.CharField(null =True, max_length=20,db_column='PassportNumber')
    PassportValidFrom = models.CharField(null =True, max_length=20,db_column='PassportValidFrom')
    PassportValidTill = models.CharField(null =True, max_length=20,db_column='PassportValidTo')
    PhysicalHandicap = models.BooleanField(null =True,default=False, db_column='Physical_Handicap')
    AccountNumber = models.CharField(null =True, max_length=20,db_column='Account_Number')
    IFSCcode = models.CharField(null =True, max_length=20,db_column='IFSC_Code')
    NameAsPerBank = models.CharField(null=True, max_length=100, db_column='Name_As_Per_Bank')
    PAN = models.CharField(null =True, max_length=20,db_column='PAN')
    NameAsPerPan = models.CharField(null=True, max_length=100, db_column='Name_As_Per_Pan')
    locomotive = models.BooleanField(null =True,default=False, db_column='locomotive')
    Hearing = models.BooleanField(null =True,default=False, db_column='Hearing')
    Visual = models.BooleanField(null =True, default=False, db_column='Visual')
    


    class Meta:
        db_table = "Candidate_PF_Details"