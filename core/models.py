import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, AbstractUser, PermissionsMixin
from django.db import models
from django.db.models import Avg


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
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    id = models.CharField(max_length=200, default=uuid.uuid4, unique=True, primary_key=True)
    username = None
    email = None
    login = models.CharField(null=False, max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserGroupRequest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class City(models.Model):
    name = models.CharField(max_length=50)


class Stadium(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    photo_link = models.CharField(max_length=200, blank=True, null=True)
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
    description = models.CharField(max_length=200, null=True, blank=True)
    photo_link = models.CharField(max_length=200, null=True, blank=True)
    contacts = models.CharField(max_length=100)
    average_mark = models.FloatField(default=0.0)

    def update_average_mark(self):
        average = self.feedback_set.aggregate(Avg('mark'))['mark__avg']
        self.average_mark = average if average is not None else 0
        self.save()


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.event.update_average_mark()

    def delete(self, *args, **kwargs):
        event = self.event
        super().delete(*args, **kwargs)
        event.update_average_mark()


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
