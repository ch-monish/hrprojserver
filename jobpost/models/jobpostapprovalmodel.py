
from django.db import models
from jobpost.models.jobpostmodel import JobPost
from managestages.models import Stage
from django.contrib.auth.models import Group

# Create your models here.

class JobPostApproval(models.Model):
    jobPostApprovalId = models.AutoField(primary_key=True, db_column='Job_Post_Approval_ID')
    jobpost = models.ForeignKey(JobPost, null =True, on_delete=models.DO_NOTHING, db_column='Job_Post_ID')
    approverName = models.CharField(max_length=20 ,  null=False, db_column='Approver_Name')
    FirstName = models.CharField(max_length=50 ,  null=False, db_column='First_Name')
    LastName = models.CharField(max_length=50  , null=False, db_column='Last_Name')    
    Email = models.CharField(max_length=100 ,  null=False, db_column='Email')
    Stage = models.ForeignKey(Stage, null =True, on_delete=models.DO_NOTHING, db_column='Stage_ID')
    role = models.ForeignKey(Group, null =True, on_delete=models.DO_NOTHING, db_column='Role_ID')
    approvalStatus = models.CharField(max_length=20 ,  null=False, db_column='Approval_Status')
    approvalDate = models.DateField(db_column='Approval_Date',  null =True, blank=True)
    approvalComments = models.CharField(max_length=1000 , null =True,  db_column='Approval_Comments')
    CreatedOn = models.DateTimeField(db_column='Created_On',  null =True, blank=True)


    class Meta:    
        db_table = 'HW_JobPost_Approval'



                      