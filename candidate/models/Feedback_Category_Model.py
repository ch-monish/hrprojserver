from django.db import models

class Feedback_Category(models.Model):
    FeedbackCategoryID=models.AutoField(primary_key=True,db_column='Feedback_Category_ID')
    InterviewType=models.CharField(max_length=40,db_column='Interview_Type')
    FeedbackCategory=models.CharField(max_length=60,db_column='Feedback_Category')
    Stage=models.CharField(max_length=200,db_column="Stage_Name",default="")
    class Meta:
        db_table="Feedback_Category"
