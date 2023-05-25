from django.db import models

class candidatecategorymodel(models.Model):
    candidatecategoryID=models.AutoField(primary_key=True,db_column="candidatecategoryID")
    categoryName=models.CharField(max_length=100,null=False)
    class meta:
        db_table="CandidateCategory"