from django.db import models

# Create your models here.

class Transpor_Type(models.Model):
    name = models.CharField(max_length=30)

class Route(models.Model):
    name = models.CharField(max_length=10)
    transport_type = models.ForeignKey(Transpor_Type)

class Traffic_Stop(models.Model):
    name = models.CharField(max_length=50)
    route = models.ManyToManyField(Route)

class Season(models.Model):
    name = models.CharField(max_length=20)

class Day_Type(models.Model):
    name = models.CharField(max_length=20)

class Time_of_Day(models.Model):
    name = models.CharField(max_length=20)

class Reasearcher(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField

class Reasearch(models.Model):
    date = models.DateTimeField
    route = models.ForeignKey(Route)
    season = models.ForeignKey(Season)
    day_type = models.ForeignKey(Day_Type)
    reasearcher = models.ForeignKey(Reasearcher)

class Reasearch_detail(models.Model):
    reasearch = models.ForeignKey(Reasearch)
    traffic_stop = models.ForeignKey(Traffic_Stop)
    time_of_day = models.ForeignKey(Time_of_Day)
    num_in = models.IntegerField
    num_out = models.IntegerField

class Result(models.Model):
    route = models.ForeignKey(Route)
    traffic_stop = models.ForeignKey(Traffic_Stop)
    season = models.ForeignKey(Season)
    day_type = models.ForeignKey(Day_Type)
    time_of_day = models.ForeignKey(Time_of_Day)
    probability = models.FloatField
    intensity = models.FloatField
    date = models.DateTimeField
