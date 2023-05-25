from django.db import models

class JobPostUserRolesModel(models.Model):

    id = models.BigIntegerField(primary_key=True)
    RoleName = models.CharField(max_length=100, db_column='Role_Name')
    UserName = models.CharField(max_length=50, db_column='User_Name')
    FullName = models.CharField(max_length=100, db_column='User_FullName')
    Email = models.CharField(max_length=100, db_column='Email')
    
    class Meta:   
        managed = False 
        db_table = 'view_user_roles'



