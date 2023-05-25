from django.db import models

# Create your models here.
class Customer(models.Model):
    CustomerId =  models.AutoField(primary_key=True, db_column='Customer_ID')
    CustomerName = models.CharField(null =False, unique=True, max_length=50, db_column='Customer_Name')
    Acronym = models.CharField(max_length=4, unique=True, null =True, db_column='Acronym')
    CustomerDesc = models.CharField(blank=True, max_length=500, db_column='Customer_Description')
    Active = models.BooleanField(default=True, db_column='Active')

    class Meta:    
        db_table = 'Customer'
