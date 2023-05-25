from django.db import models
from candidate.models.selected_Candidates_Model import Selected_Candidates
import os

class CandidateEmployementDetials(models.Model):
    
    selectedCandidateId=models.ForeignKey(Selected_Candidates,null=True,on_delete=models.DO_NOTHING,db_column="selectedCandidateId")
    PreviousCompanyName=models.CharField(max_length=40,default="",null=False)
    PreviousCompanyAddress=models.CharField(max_length=200,default="",null=True)
    Start_Date=models.DateField(null=True,blank=True)
    End_Date=models.DateField(null=True,blank=True)
    Designationonjoining=models.CharField(max_length=50,null=True)
    Designationonleaving=models.CharField(max_length=50,null=True)
    
    
    class Meta:
        db_table="CandidateEmployementDetails"


