from django.db import models

from stadium.models import Stadium


class Hall(models.Model):
    name = models.CharField(max_length=100)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
