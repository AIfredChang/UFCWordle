from django.db import models

# Create your models here.
class Fighter(models.Model):
    name = models.CharField(max_length=255)
    record = models.CharField(max_length=20)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    reach = models.CharField(max_length=10)
    stance = models.CharField(max_length=20)
    dob = models.DateField()
    def __str__(self):
        return self.name

class Event(models.Model):
    fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE)
    opponent = models.CharField(max_length=255)
    result = models.CharField(max_length=10)
    kd1 = models.IntegerField()
    kd2 = models.IntegerField()
    str1 = models.IntegerField()
    str2 = models.IntegerField()
    td1 = models.IntegerField()
    td2 = models.IntegerField()
    sub1 = models.IntegerField()
    sub2 = models.IntegerField()
    event = models.CharField(max_length=255)
    date = models.DateField()
    method = models.CharField(max_length=10)
    move = models.CharField(max_length=30)
    round = models.IntegerField()
    time = models.CharField(max_length=10)
    def __str__(self):
        return self.event