from django.db import models

# Create your models here.
class EmployementType(models.Model):
    EmployementTypeId=models.AutoField(primary_key=True,db_column="EmployementTypeId")
    EmployementType=models.CharField(unique=True,null=False,max_length=30,db_column="Employement_Type",default="")
    Active=models.BooleanField(default=True,db_column="Active",null=False)

    class Meta:
        db_table="HW_Employement_Type"