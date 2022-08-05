from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import RegexValidator

# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    phone_regx = RegexValidator(
        regex=r'^\+?0?\d{10,13}$', message='Phone number must be in correct form +2519xxxxxxxx')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    phone_no = models.CharField(validators=[phone_regx], max_length=50)

    def __str__(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()
