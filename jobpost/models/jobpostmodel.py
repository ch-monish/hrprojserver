from datetime import datetime
from django.db import models
from ManageCustomer.models import Customer
from ManageExperienceLevel.models import Experience
from ManageLocation.models import Location

from managebusinessunit.models import BusinessUnit
from managecompany.models import Company
from manageserviceline.models import ServiceLine
from ManageIndustry.models import Industry

from managestages.models import Stage

# Create your models here.

class JobPost(models.Model):
    JobPostId = models.AutoField(primary_key=True, db_column='Job_Post_ID')
    JobCode = models.CharField(max_length=20 ,  unique = True, null=False, db_column='Job_Code')
    UserName = models.CharField(max_length=20 ,  null=False, db_column='User_Name')
    FirstName = models.CharField(max_length=50 ,  null=False, db_column='First_Name')
    LastName = models.CharField(max_length=50  , null=False, db_column='Last_Name')
    Email = models.CharField(max_length=100 ,  null=False, db_column='Email')
    Stage = models.ForeignKey(Stage, null =True, on_delete=models.DO_NOTHING, db_column='Stage_Id')
    Industry = models.ForeignKey(Industry, null =True, on_delete=models.DO_NOTHING, db_column='Industry_Id')
    Company = models.ForeignKey(Company, null =True, on_delete=models.DO_NOTHING, db_column='Company_ID')
    BusinessUnit = models.ForeignKey(BusinessUnit, null =True, on_delete=models.DO_NOTHING, db_column='Business_Unit_ID')
    ServiceLine = models.ForeignKey(ServiceLine, null =True, on_delete=models.DO_NOTHING, db_column='Service_Line_ID')
    Customer = models.ForeignKey(Customer, null =True, on_delete=models.DO_NOTHING, db_column='Customer_ID')
    Location = models.ForeignKey(Location, null =True, on_delete=models.DO_NOTHING, db_column='Location_ID')
    EmploymentType = models.CharField(max_length=30  , db_column='Employment_Type')
    Duration = models.IntegerField(null=True, db_column='Dureation')
    JobTitle =models.CharField(max_length=100  , db_column='Job_Title')
    JobDesc =models.CharField(max_length=1000 , null =True,  db_column='Job_Desc')
    NoOfPositions = models.IntegerField(db_column='No_Of_Positions',null =True)
    MinimumExperiance=models.IntegerField(db_column="Minimum_Experiance",null=False,default=0,)
    MaximumExperiance=models.IntegerField(db_column="Maximum_Experiance",null=False,default=0,)
    MaximumCTC=models.IntegerField(db_column="Maximum_CTC",null=False,default=0,)

    # ExperianceLevel = models.ForeignKey(Experience, null =True, on_delete=models.DO_NOTHING, db_column='Experience_Level_ID')
    Qualification = models.CharField(max_length=30  , null =True,db_column='Qualification')
    OnBoardingDate = models.DateField(db_column='OnBoarding_Date')
    POReference = models.CharField(max_length=20  ,null =True, db_column='PO_Ref')
    CreatedBy = models.CharField(max_length=20  ,null =True, db_column='Created_By')
    CreatedOn = models.DateTimeField(db_column='Created_On',  null =True, blank=True)
    ModifiedBy = models.CharField(max_length=20,  null =True, db_column='Modified_By')
    ModifiedOn = models.DateTimeField(db_column='Modified_On', null =True, blank=True)
    Comments = models.CharField(max_length=500  , null =True,db_column='Comments')
    # jobpostapprovals=models.ManyToManyField(JobPostApproval,null=True,related_name="JobPostapprovals")
    class Meta:    
        db_table = 'HW_JobPost_Details'

  

                      