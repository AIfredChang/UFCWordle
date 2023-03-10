from django.db import models
import datetime

# Create your models here.
class Fighter(models.Model):
    name = models.CharField(max_length=255)
    record = models.CharField(max_length=20)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    reach = models.CharField(max_length=10)
    stance = models.CharField(max_length=20)
    dob = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.name

class Event(models.Model):
    fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    opponent = models.CharField(max_length=255)
    result = models.CharField(max_length=5)
    kd1 = models.IntegerField(default=0, blank=True, null=True)
    kd2 = models.IntegerField(default=0, blank=True, null=True)
    str1 = models.IntegerField(default=0, blank=True, null=True)
    str2 = models.IntegerField(default=0, blank=True, null=True)
    td1 = models.IntegerField(default=0, blank=True, null=True)
    td2 = models.IntegerField(default=0, blank=True, null=True)
    sub1 = models.IntegerField(default=0, blank=True, null=True)
    sub2 = models.IntegerField(default=0, blank=True, null=True)
    event = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)
    method = models.CharField(max_length=10)
    move = models.CharField(max_length=30)
    round = models.IntegerField()
    time = models.CharField(max_length=10)
    def __str__(self):
        return self.event