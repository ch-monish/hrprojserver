from django.db import models
from jobpost.models.jobpostmodel import JobPost
from managestages.models import Stage
import os
from ManageLocation.models import Location
from ManageExperienceLevel.models import Experience

class Candidate(models.Model):
    def get_upload_path(instance, filename):
        return os.path.join(
        instance.Jobpost.JobCode,  instance.CandidateCode, 'Resume', filename)
    Honorifics = models.CharField(max_length=5,null=True, db_column='Honorifics')
    CandidateId = models.AutoField(primary_key=True, db_column='Candidate_ID')
    CandidateCode = models.CharField(max_length=20 ,  unique = True, null=False, db_column='Candidate_Code')
    Jobpost = models.ForeignKey(JobPost, null =True, on_delete=models.DO_NOTHING, db_column='Job_Post_ID')
    HRUserName = models.CharField(max_length=20 ,  null=True, db_column='HR_User_Name')
    CanFirstName = models.CharField(max_length=50 ,  null=True, db_column='Can_First_Name')
    CanLastName = models.CharField(max_length=50  , null=True, db_column='Can_Last_Name')    
    Stage = models.ForeignKey(Stage, null =True, on_delete=models.DO_NOTHING, db_column='Stage_Id')
    Qualification = models.CharField(max_length=30  , null =True,db_column='High_Qualification')
    OverallExpYear = models.IntegerField(null=True, db_column='Overall_Exp_Year')
    OverallExpMonth = models.IntegerField(null=True, db_column='Overall_Exp_Month')
    ReleventExpYear = models.IntegerField(null=True, db_column='Relevent_Exp_Year')
    ReleventExpMonth = models.IntegerField(null=True, db_column='Relevent_Exp_Month')
    CurrentCTC = models.IntegerField(null=True, db_column='Current_CTC')
    ExpectedCTC = models.IntegerField(null=True, db_column='Expected_CTC')
    NegotiatedCTC = models.IntegerField(null=True, db_column='Negotiated_CTC')
    ExpectedDOJ = models.DateField(db_column='Expected_DOJ')
    CurrentOrganization = models.CharField(max_length=50  , null =True,db_column='Current_Org')
    CurrentJobLocation = models.CharField(max_length=50  , null =True,db_column='Current_Job_Loc')
    Skills = models.CharField(max_length=200  , null =True,db_column='Skills')
    Email = models.CharField(max_length=100 ,  null=True, db_column='Email')
    ContactNo = models.CharField(max_length=20 ,  null=True, db_column='Contact_No')
    Resume = models.FileField(upload_to=get_upload_path)
    AvgApprovedCTC = models.IntegerField(null=True, db_column='Avg_Approved_CTC')
    AvgBillRate = models.IntegerField(null=True, db_column='Avg_Bill_Rate')
    CreatedBy = models.CharField(max_length=20  ,null =True, db_column='Created_By')
    CreatedOn = models.DateTimeField(db_column='Created_On',  null =True, blank=True)
    ModifiedBy = models.CharField(max_length=20,  null =True, db_column='Modified_By')
    ModifiedOn = models.DateTimeField(db_column='Modified_On', null =True, blank=True)
    Comments=models.CharField(max_length=500,db_column="Comments",null=True,blank=True)
    Location = models.ForeignKey(Location, null =True, on_delete=models.DO_NOTHING, db_column='Location_ID')
    EmploymentType = models.CharField(null=True,max_length=30  , db_column='Employment_Type')
    Interviewer = models.CharField(null=True,max_length=150  , db_column='Interviewer')
    Internal = models.BooleanField(null=True)
    Duration = models.IntegerField(null=True, db_column='Duration')
    ExperianceLevel = models.ForeignKey(Experience, null =True, on_delete=models.DO_NOTHING, db_column='Experience_Level_ID')

   
    class Meta:    
        db_table = 'HW_Candidate_Details'
        unique_together = ('Jobpost', 'CanFirstName','CanLastName')        