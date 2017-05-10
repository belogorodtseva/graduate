from django.db import models
import weekday_field
import datetime
from datetime import date
from datetime import datetime
from django.core.exceptions import ValidationError


class Transpor_Type(models.Model):
    name = models.CharField(max_length=30)
    maxpeople = models.IntegerField(default=50)

    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=10)
    transport_type = models.ForeignKey(Transpor_Type)

    def __str__(self):
        return self.name

class Traffic_Stop(models.Model):
    name = models.CharField(max_length=50)
    route = models.ManyToManyField(Route)

    def __str__(self):
        return self.name


class Reasearch(models.Model):
    date = models.TimeField(auto_now_add=True)
    route = models.ForeignKey(Route)
    weekday = models.IntegerField(default=datetime.weekday(datetime.now()))
    month = models.IntegerField(default=datetime.now().month)


    def __str__(self):
        return str(self.date)

class Reasearch_detail(models.Model):
    numberin= models.IntegerField()
    numberout = models.IntegerField()
    reasearch = models.ForeignKey(Reasearch)
    traffic_stop = models.ForeignKey(Traffic_Stop)
    time = models.TimeField(auto_now_add = True)


class Check(models.Model):
    SEASONS = (
        ('W', 'Winter'),
        ('S', 'Summer'),
        ('A', 'Autumn'),
        ('Sp','Spring'),
    )
    DAYTYPES = (
        ('W', 'Workday'),
        ('F', 'Friday'),
        ('O', 'Day Out'),
    )
    season = models.CharField(max_length=2, choices=SEASONS)
    daytype = models.CharField(max_length=1, choices=DAYTYPES)
    route = models.ForeignKey(Route)
    timestart = models.TimeField(auto_now=False)
    timeend = models.TimeField(auto_now=False)

    def clean(self):
        " Make sure date not in the past "
        if self.timestart > self.timeend :
            raise ValidationError('TIME END < TIME START')

class ReasearchStand(models.Model):
    date = models.TimeField(auto_now_add=True)
    route = models.ForeignKey(Route)
    weekday = models.IntegerField(default=datetime.weekday(datetime.now()))
    month = models.IntegerField(default=datetime.now().month)


    def __str__(self):
        return str(self.date)

class ReasearchStand_detail(models.Model):
    numbercome= models.IntegerField()
    reasearch = models.ForeignKey(ReasearchStand)
    traffic_stop = models.ForeignKey(Traffic_Stop)
    timewait = models.IntegerField()
