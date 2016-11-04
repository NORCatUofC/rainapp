from django.db import models


class HourlyPrecip(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    precip = models.FloatField()
