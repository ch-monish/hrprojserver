from django.db import models

from ManageExperienceLevel.models import Experience

class CandidateActionModel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    CandidateApprovalID = models.BigIntegerField(db_column='Candidate_Approval_ID')
    RoleName = models.CharField(max_length=50, db_column='Role_Name')
    CandidateId = models.BigIntegerField(db_column='Candidate_ID')
    CandidateCode = models.CharField(max_length=100, db_column='Candidate_Code')
    Honorifics = models.CharField(max_length=5, db_column='Honorifics')
    CanFirstName = models.CharField(max_length=100, db_column='Can_First_Name')
    CanLastName = models.CharField(max_length=100, db_column='Can_Last_Name')
    CandidateName = models.CharField(max_length=200, db_column='Can_Name')
    ContactNo = models.CharField(max_length=10, db_column='Contact_No')
    CurrentCTC = models.IntegerField(db_column='Current_CTC')
    ExpectedCTC = models.IntegerField(db_column='Expected_CTC')
    NegotiatedCTC = models.IntegerField(db_column='Negotiated_CTC')
    Skills = models.CharField(max_length=500, db_column='Skills')
    Resume = models.CharField(max_length=10000,db_column='Can_Resume')
    CurrentOrganization = models.CharField(max_length=200, db_column='Current_Org')
    CurrentJobLocation = models.CharField(max_length=100, db_column='Current_Job_Loc')
    Email = models.CharField(max_length=100, db_column='Email')
    ExpectedDOJ = models.DateField(db_column='Expected_DOJ')
    OverallExpYear = models.IntegerField(null=True, db_column='Overall_Exp_Year')
    OverallExpMonth = models.IntegerField(null=True, db_column='Overall_Exp_Month')
    ReleventExpYear = models.IntegerField(null=True, db_column='Relevent_Exp_Year')
    ReleventExpMonth = models.IntegerField(null=True, db_column='Relevent_Exp_Month')
    CandidateReleventExp = models.CharField(max_length=50,db_column='CAN_Relevent_Exp')
    CandidateOverallExp = models.CharField(max_length=50,db_column='CAN_Overall_Exp')
    Qualification = models.CharField(max_length=100, db_column='High_Qualification')
    AvgApprovedCTC = models.IntegerField(db_column='Can_Avg_Approved_CTC')
    AvgBillRate = models.IntegerField(db_column='Can_Avg_Bill_Rate')
    ExperianceLevel = models.ForeignKey(Experience, null =True, on_delete=models.CASCADE, db_column='Experience_Level_ID')

    # JobPostApprovalID = models.BigIntegerField(db_column='Job_Post_Approval_ID')
    JobPostID = models.BigIntegerField(db_column='Job_Post_ID')
    JobCode = models.CharField(max_length=100, db_column='Job_Code')
    UserName = models.CharField(max_length=50, db_column='User_Name')
    HiringManager = models.CharField(max_length=100, db_column='Hiring_Manager')
    ApproverName = models.CharField(max_length=50, db_column='Approver_Name')
    ApproverDisplayName = models.CharField(max_length=100, db_column='Approver_Display_Name')
    ApproverEmail = models.CharField(max_length=100, db_column='Approver_Email')    
    JobTitle =models.CharField(max_length=100, db_column='Job_Title')
    JobDesc =models.CharField(max_length=1000, db_column='Job_Desc')
    EmploymentType = models.CharField(max_length=50, db_column='Employment_Type')
    Duration = models.IntegerField(db_column='Dureation')
    NoOfPositions = models.IntegerField(db_column='No_Of_Positions')
    Qualification = models.CharField(max_length=50, db_column='Qualification')
    OnBoardingDate = models.DateField(db_column='OnBoarding_Date')
    POReference = models.CharField(max_length=50, db_column='PO_Ref')
    stage_name = models.CharField(max_length=50, db_column='Stage_Name')
    StageDesc = models.CharField(max_length=100, db_column='Satge_Desc')
    industry_name =  models.CharField(max_length=100, db_column='Industry_Name')
    company_name = models.CharField(max_length=50, db_column='Company_Name')
    businessunit_name = models.CharField(max_length=50, db_column='Business_Unit_Name')
    serviceline_name = models.CharField(max_length=50, db_column='Service_Line_Name')
    customer_name = models.CharField(max_length=50, db_column='Customer_Name')
    location_name = models.CharField(max_length=50, db_column='Location_Name')
    ExperianceLevel = models.ForeignKey(Experience, null =True, on_delete=models.DO_NOTHING, db_column='Experience_Level')
    DefAvgApprovedCTC = models.IntegerField(db_column='Avg_Approved_CTC')
    DefAvgBillRate = models.IntegerField(db_column='Avg_Bill_Rate')
    MinimumExperiance = models.IntegerField(db_column='Minimum_Experiance')
    MaximumExperiance = models.IntegerField(db_column='Maximum_Experiance')
    MaximumCTC = models.IntegerField(db_column='Maximum_CTC')
    Location=models.IntegerField(db_column="Can_Location_ID")
    CanJobLocation = models.CharField(max_length=50, db_column='Can_Location_Name')
    CanEmploymentType = models.CharField(max_length=50, db_column='Can_Employment_Type')
    CanDuration = models.IntegerField(db_column='Can_Duration')
    class Meta:   
        managed = False 
        db_table = 'view_candidateaction'