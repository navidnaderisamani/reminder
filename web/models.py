from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class Expense(models.Model):

    text = models.CharField(max_length = 255, default='')
    dong = models.CharField(max_length = 255, default='',null=True, blank=True)
    amount = models.BigIntegerField(default = '')
    user = models.ForeignKey(User, default = '')
    date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return (self.text)

class Income(models.Model):

    text = models.CharField(max_length = 255, default='')
    amount = models.BigIntegerField(default = '')
    user = models.ForeignKey(User, default = '')
    date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '{}{}'.format(self.text, self.date)


class Token(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE)
    token = models.CharField(max_length = 200)

    def __unicode__(self):
        return "{}_token".format(self.user )

class Passwordresetcodes(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=120)
    time = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)  # TODO: do not save password

class Plan(models.Model):
    time = models.DateTimeField()
    saturday = models.CharField(max_length = 255)
    sunday = models.CharField(max_length = 255)
    monday = models.CharField(max_length = 255)
    tuesday = models.CharField(max_length = 255)
    wednesday = models.CharField(max_length = 255)
    thursday = models.CharField(max_length = 255)
    friday = models.CharField(max_length = 255)
