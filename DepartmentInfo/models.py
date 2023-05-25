from django.db import models

# Create your models here.
class DepartmentInformation(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ID')
    Email = models.CharField(null=False, max_length=200, db_column='Email')
    Department = models.CharField(null=False, max_length=100, db_column='Department')

    class Meta:
        db_table = 'Department_Information'
class BGVVendors(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ID')
    Email = models.CharField(null=False, max_length=200, db_column='Email')
    Bgvvendor = models.CharField(null=False, max_length=100, db_column='Bgvvendor')
    class Meta:
        db_table="BGVVendors"