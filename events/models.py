from django.db import models


class HourlyPrecip(models.Model):
    start_time = models.DateTimeField(unique=True)
    end_time = models.DateTimeField(unique=True)
    precip = models.FloatField()
