from django.db import models

# Create your models here.
class Band(models.Model):
    BandId = models.AutoField(primary_key=True, db_column='Band_ID')
    BandName = models.CharField(null =False, unique=True, max_length=10, db_column='Band_Name')
    BandDesc = models.CharField(blank=True, max_length=10, db_column='Band_Desc')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Band'