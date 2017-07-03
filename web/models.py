from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Expense(models.Model):

    text = models.CharField(max_length = 255, default='')
    dong = models.CharField(max_length = 255, default='')
    amount = models.BigIntegerField(default = '')
    user = models.ForeignKey(User, default = '')
    


class Income(models.Model):

    text = models.CharField(max_length = 255, default='')
    dong = models.CharField(max_length = 255, default='')
    amount = models.BigIntegerField(default = '')
    user = models.ForeignKey(User, default = '')
