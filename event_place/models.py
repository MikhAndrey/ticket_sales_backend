from django.contrib.auth.models import User
from django.db import models

from event.models import Event
from place.models import Place
from purchase.models import Purchase


class EventPlace(models.Model):
    class Meta:
        unique_together = (('event', 'place'),)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    price = models.FloatField()
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True)
