from django.db import models

# Create your models here.
class Company (models.Model):
    CompanyId = models.AutoField(primary_key=True, db_column='Company_ID')
    CompanyName = models.CharField(max_length=50, unique = True, db_column='Company_Name')
    CompanyDesc = models.CharField(max_length=500, blank=True, db_column='Company_Desc')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Company'

