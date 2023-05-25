from django.db import models

# Create your models here.
class Location(models.Model):
    LocationId =  models.AutoField(primary_key=True, db_column='Location_ID')
    LocationName = models.CharField(null =False, unique=True, max_length=50, db_column='Location_Name')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Location'