from django.db import models
from candidate.models.Feedback_Category_Model import Feedback_Category
from candidate.models.candidatemodel import Candidate


class Candidate_Feedback(models.Model):
    CandidateFeedbackID=models.AutoField(primary_key=True)
    Candidate=models.ForeignKey(Candidate,null=True,on_delete=models.DO_NOTHING,db_column="Candidate_ID")
    FeedbackCategory=models.ForeignKey(Feedback_Category,null=True,on_delete=models.DO_NOTHING,db_column="Feedback_Category_ID")
    Comments=models.CharField(max_length=500,null=True)
    Rating=models.IntegerField(null=True)
    class Meta:
        db_table="Candidate_Feedback"