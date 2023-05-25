from django.db import models
from candidate.models.selected_Candidates_Model import Selected_Candidates

class CandidateFamilyDetails(models.Model):
    selectedCandidateId=models.ForeignKey(Selected_Candidates,null=True,on_delete=models.DO_NOTHING,db_column="selectedCandidateId")
    FullName=models.CharField(null=True,max_length=40)
    Date_Of_Birth=models.DateField(null=True)
    Relationship_with_employee=models.CharField(null=True,max_length=20)
    Contact_Number=models.CharField(null=True,max_length=15)
    class Meta:
        db_table="CandidateFamilyDetails"
