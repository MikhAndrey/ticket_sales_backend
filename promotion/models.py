from django.db import models


class Promotion(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount = models.FloatField()
