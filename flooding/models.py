from django.db import models


class BasementFloodingEvent(models.Model):

    UNIT_TYPE = (
        ('z', 'zip'),
        ('c', 'community'),
        ('w', 'ward')
    )

    date = models.DateField()
    unit_type = models.CharField(choices=UNIT_TYPE, max_length=1)
    unit_id = models.CharField(max_length=20)
    count = models.IntegerField()

    class Meta:
        unique_together = ('date', 'unit_type', 'unit_id')
