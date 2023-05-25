from django.db import models
from candidate.models.selected_Candidates_Model import Selected_Candidates
import os

class CandidateEducationalDetails(models.Model):
    selectedCandidateId=models.ForeignKey(Selected_Candidates,null=True,on_delete=models.DO_NOTHING,db_column="selectedCandidateId")
    Qualification=models.CharField(max_length=50,null=False,db_column="Qualification")
    Specialization=models.CharField(max_length=50,null=True,db_column="Specialization")
    Start_Date=models.DateField(null=True,blank=True,db_column="Start_Date")
    End_Date=models.DateField(null=True,blank=True,db_column="End_Date")
    Institute=models.CharField(null=True,max_length=100,db_column="Institute")
    Percentage=models.CharField(null=True,max_length=5,db_column="Percentage")
    
    class Meta:
        db_table="CandidateEducationalDetails"


