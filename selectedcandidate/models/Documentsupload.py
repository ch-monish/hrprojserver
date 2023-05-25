from django.db import models

import os
from candidate.models.selected_Candidates_Model import Selected_Candidates


class CandidateDocumentsUpload(models.Model):
    def get_upload_path(instance, filename):
        return os.path.join(str(instance.selectedcandidate.candidate.Jobpost.JobCode),str(instance.selectedcandidate.candidate.CandidateCode), str(instance.detailtype),filename)
    selectedcandidate = models.ForeignKey(Selected_Candidates,on_delete=models.DO_NOTHING, db_column='selectedCandidateId')
    detailtypeId=models.IntegerField(null=True)
    detailtype=models.CharField(null=False,max_length=30)
    file=models.FileField(upload_to=get_upload_path,db_column="documentpath", max_length=300)
    verified=models.CharField(null=True,max_length=80,default=None)
    verificationcomments=models.CharField(null=True,max_length=80)
    class Meta:
        db_table="CandidateDocuments"