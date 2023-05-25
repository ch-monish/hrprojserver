from django.db import models
from candidate.models.selected_Candidates_Model import Selected_Candidates

class CandidateInsuranceDetails(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ID')
    Selected_Candidate_ID=models.ForeignKey(Selected_Candidates,null=True,on_delete=models.DO_NOTHING,db_column="Selected_Candidate_ID")
    Name=models.CharField(max_length=50,null=False,db_column='Name')
    DateOfBirth=models.DateField(null=True,blank=True,db_column='DoB')
    Age=models.IntegerField(null=True,blank=True,db_column="Age")
    Relationship=models.CharField(null=True,max_length=30,db_column='Relationship')
    Gender=models.CharField(max_length=15,null=True,db_column='Gender')
    Age=models.CharField(max_length=2,null=True,db_column='Age')
    # PercentageofInsurance=models.IntegerField(null=True,default=100,db_column='PercentageofInsurance')
    
    
    class Meta:
        db_table="CandidateInsuranceDetails"


