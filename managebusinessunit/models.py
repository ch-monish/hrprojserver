from django.db import models

# Create your models here.
class BusinessUnit (models.Model):
    BusinessUnitId = models.AutoField(primary_key=True, db_column='Business_Unit_ID')
    CompanyId = models.IntegerField(null=False, db_column='Company_ID')
    BusinessUnitName = models.CharField(max_length=50, null =False, db_column='Business_Unit_Name')
    BusinessUnitDesc = models.CharField(max_length=500, blank=True, db_column='Business_Unit_Desc')
    HR=models.CharField(null=True,max_length=40,db_column="HR")
    Acronym = models.CharField(max_length=4, null=True, db_column='Acronym', unique=True)
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Business_Unit'
        unique_together = ('CompanyId', 'BusinessUnitName')