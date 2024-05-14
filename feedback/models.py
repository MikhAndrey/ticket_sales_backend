from django.db import models

from event.models import Event
from user.models import User


class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date = models.DateTimeField()
    mark = models.IntegerField()
