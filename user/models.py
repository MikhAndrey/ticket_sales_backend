import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
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
