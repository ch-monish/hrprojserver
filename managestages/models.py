
from tokenize import group
from django.db import models
from django.contrib.auth.models import Group

# Create your models here.
class Stage (models.Model):
    Id = models.AutoField(primary_key=True,  db_column='Id')
    StageType = models.CharField(max_length=50, null =False, db_column='Stage_Type')
    # StageId = models.IntegerField(null =False, db_column='Stage_Id')
    StageName = models.CharField(max_length=50, null =False, db_column='Stage_Name')
    StageDesc = models.CharField(max_length=200, null =False, db_column='Satge_Desc')
    # StageRole = models.ForeignKey(Group, null =True, on_delete=models.DO_NOTHING)

    class Meta:    
        db_table = 'HW_Stage'

