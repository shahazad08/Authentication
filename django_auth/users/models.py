from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given name must be set")
        try:
            with transaction.atomic():
                user = self.model(username, **extra_fields)
                user.set_password(password)
                user.save(self._db)
                return user
        except:
            raise

    def create_user(self,username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password=password, **extra_fields)






class User(AbstractBaseUser, PermissionsMixin):  # User model is the built-in Django model that provides
    # us with username , email , password , first_name , and last_name fields.
    username=models.CharField(max_length=40,unique=True)
    email = models.EmailField(max_length=40)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    object = UserManager()     # Created the object of the User Manager module which contains the fields..

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

# Create your models here.
