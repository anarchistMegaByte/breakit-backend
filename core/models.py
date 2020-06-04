from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('username',)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(self.phone_number)

        if not self.password:
            self.set_unusable_password()

        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.phone_number)
