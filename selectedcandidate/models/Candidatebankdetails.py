from django.db import models
from candidate.models.selected_Candidates_Model import  Selected_Candidates
import os
# Create your models here.
class CandidateBankDetails(models.Model):
    def get_upload_path(instance,filename):
        return os.path.join(str(instance.selectedcandidateid.candidate.Jobpost.JobCode),str(instance.selectedcandidateid.candidate.CandidateCode),"Bankdetials",filename)
    Id = models.AutoField(primary_key=True, db_column='ID')
    selectedcandidateid=models.ForeignKey(Selected_Candidates,null=True,on_delete=models.DO_NOTHING,db_column="selectedcandidateid")
    BankName = models.CharField(null=False, max_length=100, db_column='Bank_Name')
    AccountNumber = models.CharField(null = False, max_length=100,db_column='Account_Number')
    BranchName =  models.CharField(null=False, max_length=100, db_column='Branch_Name')
    IFSCcode = models.CharField(null=False, max_length=100, db_column='IFSC_Code')
    BankPassbook = models.FileField(upload_to=get_upload_path,null=True, db_column='Bank_Passbook')
    
    class Meta:    
        db_table = 'Candidate_Bank_Details'