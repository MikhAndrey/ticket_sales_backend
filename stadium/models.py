from django.db import models

from city.models import City


class Stadium(models.Model):
    models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    photo_link = models.CharField(max_length=200)
    contacts = models.CharField(max_length=100)
