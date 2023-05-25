from datetime import datetime
from django.db import models
from ManageCustomer.models import Customer
from ManageExperienceLevel.models import Experience
from ManageLocation.models import Location
from managebusinessunit.models import BusinessUnit
from managecompany.models import Company
from manageserviceline.models import ServiceLine

from managestages.models import Stage

# Create your models here.
    

class JobPostActionModel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    JobPostApprovalID = models.BigIntegerField(db_column='Job_Post_Approval_ID')
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
    Stage = models.CharField(max_length=50, db_column='Stage_Name')
    StageDesc = models.CharField(max_length=100, db_column='Satge_Desc')
    industry_name =  models.CharField(max_length=100, db_column='Industry_Name')
    company_name = models.CharField(max_length=50, db_column='Company_Name')
    businessunit_name = models.CharField(max_length=50, db_column='Business_Unit_Name')
    serviceline_name = models.CharField(max_length=50, db_column='Service_Line_Name')
    customer_name = models.CharField(max_length=50, db_column='Customer_Name')
    Business_Unit_ID=models.IntegerField(db_column="Business_Unit_ID")
    Company_ID=models.IntegerField(db_column="Company_ID")
    Service_Line_ID=models.IntegerField(db_column="Service_Line_ID")
    Location_ID=models.IntegerField(db_column="Location_ID")
    location_name = models.CharField(max_length=50, db_column='Location_Name')
    # experience_Level = models.CharField(max_length=50, db_column='Experience_Level')
    # AvgApprovedCTC=models.FloatField(db_column="Avg_Approved_CTC")
    # AvgBillRate=models.FloatField(db_column="Avg_Bill_Rate")
    experience_range = models.CharField(max_length=50, db_column='Experiance_Range')
    MaximumExperiance=models.FloatField(db_column="Maximum_Experiance")
    MinimumExperiance=models.FloatField(db_column="Minimum_Experiance")
    MaximumCTC=models.FloatField(db_column="Maximum_CTC")

    class Meta:   
        managed = False 
        db_table = 'view_jobpostaction'

                      