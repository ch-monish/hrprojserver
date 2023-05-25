from django.db import models

# Create your models here.
class Designation(models.Model):
    DesignationId = models.AutoField(primary_key=True, db_column='Designation_ID')
    DesignationName = models.CharField(null =False, unique=True, max_length=100, db_column='Designation_Name')
    DesignationDesc =  models.CharField(blank=True, max_length=500, db_column='Designation_Desc')
    Active = models.BooleanField(default=True, null =True, db_column='Active')

    class Meta:    
        db_table = 'Designation'
