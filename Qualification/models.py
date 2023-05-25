from django.db import models

# Create your models here.

class Qualification(models.Model):
    QualificationId=models.AutoField(primary_key=True,db_column="Qualification_Id")
    Qualification=models.CharField(unique=True,null=False,max_length=30,db_column='Qualification',default="")
    Active=models.BooleanField(default=True,null=False,db_column="Active")
    class Meta:
        db_table="HW_Qualifications"