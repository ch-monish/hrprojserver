from django.db import models

class JobPostStakeHolders(models.Model):
    JobPostId = models.BigIntegerField(db_column='Job_Post_ID', primary_key=True)
    HMusername = models.CharField(max_length=100, db_column='Hiring_Manager')
    HMname = models.CharField(max_length=100, db_column='Hiring_Manager_Name')
    HMemail = models.CharField(max_length=100, db_column='Hiring_Manager_Email')
    BHusername = models.CharField(max_length=100, db_column='Business_Head')
    BHname = models.CharField(max_length=100, db_column='Business_Head_Name')
    BHemail = models.CharField(max_length=100, db_column='Business_Head_Email')
    Recruiterusername = models.CharField(max_length=100, db_column='Recruiter')
    RecruiterName = models.CharField(max_length=100, db_column='Recruiter_Name')
    RecruiterEmail = models.CharField(max_length=100, db_column='Recruiter_Email')
    IndustryHeadusername = models.CharField(max_length=100, db_column='Industry_Head')
    IndustryHeadName = models.CharField(max_length=100, db_column='Industry_Head_Name')
    IndustryHeadEmail = models.CharField(max_length=100, db_column='Industry_Head_Email')
    HRusername = models.CharField(max_length=100, db_column='HR')
    HRName = models.CharField(max_length=100, db_column='HR_Name')
    HREmail = models.CharField(max_length=100, db_column='HR_Email')
    class Meta:   
        managed = False 
        db_table = 'view_jobpoststakeholders'






