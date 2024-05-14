from django.db import models

from event.models import Event


class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)
