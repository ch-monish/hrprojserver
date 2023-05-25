from django.db import models

# Create your models here.
class Insurance (models.Model):
    InsuranceAccidentLimitId = models.AutoField(primary_key=True, db_column='Insurance_Accident_Limit_ID')
    BandId = models.IntegerField(null=False, unique=True, db_column='Band_ID')
    InsuranceLimit = models.FloatField(default=0,null=False, db_column='Insurance_Limit')
    AccidentLimit = models.FloatField(default=0,null=False, db_column='Accident_Limit')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Insurance'