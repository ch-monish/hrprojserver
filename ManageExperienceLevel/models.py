from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Experience (models.Model):
    ExperienceLevelId = models.AutoField(primary_key=True, db_column='Experience_Level_ID')
    ExperienceLevel =  models.CharField(null=False, unique=True, max_length=100, db_column='Experience_Level')
    Min_Experience = models.IntegerField(null=False, db_column='Min_ExperienceRange')
    Max_Experience = models.IntegerField(null=False, db_column='Max_ExperienceRange')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Experience'
