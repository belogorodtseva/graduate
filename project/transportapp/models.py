from django.db import models


class Transpor_Type(models.Model):
    name = models.CharField(max_length=30)

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

class Season(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Day_Type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Time_of_Day(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Reasearcher(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField

    def __str__(self):
        return self.name

class Reasearch(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    route = models.ForeignKey(Route)
    season = models.ForeignKey(Season)
    day_type = models.ForeignKey(Day_Type)
    reasearcher = models.ForeignKey(Reasearcher)



class Reasearch_detail(models.Model):
    numberin= models.IntegerField()
    numberout = models.IntegerField()
    reasearch = models.ForeignKey(Reasearch)
    traffic_stop = models.ForeignKey(Traffic_Stop)
    time = models.TimeField(auto_now_add = True)



class Result(models.Model):
    route = models.ForeignKey(Route)
    traffic_stop = models.ForeignKey(Traffic_Stop)
    season = models.ForeignKey(Season)
    day_type = models.ForeignKey(Day_Type)
    time_of_day = models.ForeignKey(Time_of_Day)
    probability = models.FloatField
    intensity = models.FloatField
    date = models.DateTimeField()

class ReasearchStand(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    route = models.ForeignKey(Route)
    season = models.ForeignKey(Season)
    day_type = models.ForeignKey(Day_Type)
    reasearcher = models.ForeignKey(Reasearcher)

class ReasearchStand_detail(models.Model):
    numbercome= models.IntegerField()
    reasearch = models.ForeignKey(Reasearch)
    traffic_stop = models.ForeignKey(Traffic_Stop)
    timewait = models.IntegerField()
