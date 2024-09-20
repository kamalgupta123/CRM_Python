from django.db import models  

class Employee(models.Model):
    companyID = models.CharField(max_length=50, blank=True)
    SalesEmployeeCode = models.CharField(max_length=20, blank=True)
    SalesEmployeeName = models.CharField(max_length=50, blank=True)
    EmployeeID = models.CharField(max_length=30, blank=True)
    userName = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=30, blank=True)
    firstName = models.CharField(max_length=20, blank=True)
    middleName = models.CharField(max_length=20, blank=True)
    lastName = models.CharField(max_length=20, blank=True)
    Email = models.CharField(max_length=35, blank=True)
    Mobile = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=20, blank=True)
    Active = models.CharField(max_length=20, blank=True)
    passwordUpdatedOn = models.CharField(max_length=30, blank=True)
    lastLoginOn = models.CharField(max_length=30, blank=True)
    logedIn = models.CharField(max_length=20, blank=True)
    reportingTo = models.CharField(max_length=20, blank=True)
    FCM = models.CharField(max_length=250, blank=True)
    timestamp = models.CharField(max_length=30, blank=True)


class Target(models.Model):
    amount = models.FloatField(default=0)
    monthYear = models.CharField(max_length=50, blank=True)
    SalesPersonCode = models.IntegerField(default=0)
    sale = models.FloatField(default=0)
    sale_diff = models.FloatField(default=0)
    CreatedDate = models.CharField(max_length=20, blank=True)
    UpdatedDate = models.CharField(max_length=20, blank=True)
    