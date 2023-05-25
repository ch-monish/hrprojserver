from django.db import models
from candidate.models.selected_Candidates_Model  import Selected_Candidates
# Create your models here.
class Operationalmails(models.Model):
    selectedcandidateid=models.ForeignKey(Selected_Candidates,on_delete=models.DO_NOTHING,db_column="Selected_Candidate_ID")
    mailcategory=models.CharField(null=True,max_length=100)
    mailsent=models.BooleanField(null=False,default=False)
    mailsentat=models.DateField(null=True,blank=True)
    mailssentto=models.CharField(null=True,max_length=500)
    class Meta:
        db_table="Operational_Mails"