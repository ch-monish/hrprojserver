from django.db import models

# Create your models here.
class ServiceLine (models.Model):
    ServiceLineId = models.AutoField(primary_key=True, db_column='Service_Line_ID')
    CompanyId = models.IntegerField(null=False, db_column='Company_ID')
    BusinessUnitId = models.IntegerField(null=False, db_column='Business_Unit_ID')
    ServiceLineName = models.CharField(max_length=50, null=False, db_column='Service_Line_Name')
    Acronym = models.CharField(max_length=4, null=True, db_column='Acronym')
    ServiceLineDesc = models.CharField(max_length=500, blank=True, db_column='Service_Line_Desc')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'ServiceLine'
        unique_together = ('CompanyId', 'BusinessUnitId', 'ServiceLineName')

        