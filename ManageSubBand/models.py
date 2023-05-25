from django.db import models

# Create your models here.
class SubBand(models.Model):
    SubBandId = models.AutoField(primary_key=True, db_column='Sub_Band_ID')
    SubBandName = models.CharField(null =False, unique=True, max_length=5, db_column='Sub_Band_Name')
    BandId = models.IntegerField(null=False, db_column='Band_ID')
    SubBandDesc = models.CharField(blank =True, max_length=500, db_column='Sub_Band_Desc')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'SubBand'
        unique_together = ('SubBandName', 'BandId')
        