import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Group
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, login, password=None):
        user = self.model(
            login=login
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None):
        user = self.create_user(
            login=login,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.CharField(max_length=200, default=uuid.uuid4, unique=True, primary_key=True)
    login = models.CharField(null=False, max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    requested_role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'login'

    objects = UserManager()


class City(models.Model):
    name = models.CharField(max_length=50)


class Stadium(models.Model):
    models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    photo_link = models.CharField(max_length=200)
    contacts = models.CharField(max_length=100)


class Hall(models.Model):
    name = models.CharField(max_length=100)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)


class Purchase(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('purchased', 'Purchased'),
    )
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='booked')


class Event(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    photo_link = models.CharField(max_length=200)
    contacts = models.CharField(max_length=100)
    average_mark = models.FloatField()


class Place(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    sector = models.IntegerField()
    row = models.IntegerField()
    seat = models.IntegerField()
    x_offset = models.FloatField()
    y_offset = models.FloatField()


class EventPlace(models.Model):
    class Meta:
        unique_together = (('event', 'place'),)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    price = models.FloatField()
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True)


class EventRequest(models.Model):
    STATUS_CHOICES = (
        ('in_review', 'In review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_review')


class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date = models.DateTimeField()
    mark = models.IntegerField()


class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)


class Video(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)


class Promotion(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount = models.FloatField()


class PromotionEvent(models.Model):
    class Meta:
        unique_together = (('promotion', 'event'),)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
