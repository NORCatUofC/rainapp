from django.db import models


class RiverOutfall(models.Model):
    name = models.TextField()
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)


class RiverCso(models.Model):
    river_outfall = models.ForeignKey("RiverOutfall")
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
