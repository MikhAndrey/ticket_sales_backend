from django.db import models

from hall.models import Hall


class Place(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    sector = models.IntegerField()
    row = models.IntegerField()
    seat = models.IntegerField()
    x_offset = models.FloatField()
    y_offset = models.FloatField()
