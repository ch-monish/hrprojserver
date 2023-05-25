from django.db import models

# Create your models here.

class AdUsers(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ID')
    UserName = models.CharField(null=False, max_length=50, db_column='User_Name')
    FirstName = models.CharField(null=False, max_length=50, db_column='First_Name')
    LastName = models.CharField(null=False, max_length=50, db_column='Last_Name')
    Email = models.CharField(null=False, max_length=100, db_column='Email')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Ad_Users'
        unique_together = ('UserName', 'FirstName', 'LastName', 'Email')
        