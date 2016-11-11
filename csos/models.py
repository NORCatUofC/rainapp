from django.db import models


class RiverOutfall(models.Model):
    name = models.TextField()
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)


class RiverCso(models.Model):
    river_outfall = models.ForeignKey("RiverOutfall")
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()


class LakeOutfall(models.Model):
    name = models.TextField()
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)


class LakeReversal(models.Model):
    lake_outfall = models.ForeignKey("LakeOutfall")
    open_date = models.DateTimeField()
    close_date = models.DateTimeField()
    millions_of_gallons = models.FloatField()
