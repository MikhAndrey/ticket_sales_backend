from django.db import models

from event.models import Event


class EventRequest(models.Model):
    STATUS_CHOICES = (
        ('in_review', 'In review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_review')
