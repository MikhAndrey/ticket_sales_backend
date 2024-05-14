from django.db import models

from hall.models import Hall


class Event(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    photo_link = models.CharField(max_length=200)
    contacts = models.CharField(max_length=100)
    average_mark = models.FloatField()
