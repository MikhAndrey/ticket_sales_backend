from django.db import models

from user.models import User


class Purchase(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('purchased', 'Purchased'),
    )
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='booked')
