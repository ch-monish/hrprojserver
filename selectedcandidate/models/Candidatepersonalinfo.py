from django.db import models
from candidate.models.selected_Candidates_Model import Selected_Candidates

class CandidatePersonalInfo(models.Model):
    selectedCandidateid=models.ForeignKey(Selected_Candidates,null=True,on_delete=models.DO_NOTHING,db_column="Selected_Candidate_ID")
    Name=models.CharField(max_length=40,null=False)
    DateOfBirth=models.DateField(null=True,blank=True)
    Marital_status=models.CharField(max_length=40,null=True,blank=True)
    Gender=models.CharField(null=True,max_length=30)
    BloodGroup=models.CharField(null=True,max_length=5)
    PAN=models.CharField(null=True,max_length=10)
    AADHAR=models.CharField(null=True,max_length=20)
    Email=models.CharField(null=True,max_length=50)
    ContactNumber=models.CharField(null=True,max_length=15)
    EmergencycontactName=models.CharField(null=True,max_length=40)
    EmergencycontactRelation=models.CharField(null=True,max_length=20)
    EmergencycontactNumber=models.CharField(null=True,max_length=20)
    PassportNumber=models.CharField(null=True,max_length=20)
    PassportValidFrom=models.DateField(null=True)
    PassportValidTo=models.DateField(null=True)
    Address=models.CharField(null=True,max_length=500)
    class Meta:
        db_table="CandidatePersonalInfo"


