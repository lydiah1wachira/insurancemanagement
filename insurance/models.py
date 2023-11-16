from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer


class Category(models.Model):
    '''Model class to help create Category objects'''
    category_name = models.CharField(max_length=20)
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.category_name


class Policy(models.Model):
    ''' Model class to create Policy objects'''
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    policy_name = models.CharField(max_length=200)
    sum_assurance = models.PositiveIntegerField()
    premium = models.PositiveIntegerField()
    tenure = models.PositiveIntegerField()
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.policy_name


class PolicyRecord(models.Model):
    '''Model class to create PolicyRecords Objects'''
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="Pending")
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.policy


class Question(models.Model):
    '''Model class to create Question Objects'''
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    admin_comment = models.CharField(max_length=200, default="Nothing")
    asked_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.description
    
