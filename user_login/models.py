from django.db import models

# Create your models here.
class User_Purchase_List(models.Model):
    company_name = models.CharField(max_length=255, unique=False)
    user_name = models.CharField(max_length=255, unique=False)
    user_email = models.CharField(max_length=50, unique=False)
    company_phone = models.CharField(max_length=30, unique=False)
    company_email = models.CharField(max_length=50, unique=True)
    ad_price = models.FloatField(unique=False)
    ad_name = models.CharField(max_length=255, unique=False)
    purchase_date  = models.DateField(unique=False)
    rating = models.IntegerField(null = True, unique=False)
    active = models.IntegerField(unique=False)
    complaint = models.CharField(max_length=1023, null = True, unique=False)
    response = models.CharField(max_length=1023, null=True, unique=False)
    address = models.CharField(max_length=1023, null=True, unique=False)