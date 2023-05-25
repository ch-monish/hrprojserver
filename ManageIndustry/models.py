from django.db import models

# Create your models here.
class Industry(models.Model):
    IndustryId = models.AutoField(primary_key=True, db_column='Industry_ID')
    IndustryName = models.CharField(null = False, unique=True, max_length=100, db_column='Industry_Name')
    IndustryDesc = models.CharField(blank=True, max_length=500, db_column='Industry_Desc')
    IndustryHead=models.CharField(null=True,max_length=40,db_column="Industry_Head")
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Industry'
        