from django.db import models


class HourlyPrecip(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    precip = models.FloatField()


class NYearEvent(models.Model):
    n = models.IntegerField()
    duration_hours = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    inches = models.FloatField()
