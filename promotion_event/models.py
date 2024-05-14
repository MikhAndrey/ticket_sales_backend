from django.db import models

from event.models import Event
from promotion.models import Promotion


class PromotionEvent(models.Model):
    class Meta:
        unique_together = (('promotion', 'event'),)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
