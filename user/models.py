import os
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

def user_image_field(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join('uploads', 'user', filename)

# Create your models here.

# Client 
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    url_image = models.ImageField(null=True, upload_to=user_image_field)
    password = models.CharField(max_length=255)
    declared_salary = models.DecimalField()

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Adress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    state = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    city = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    cep = models.IntegerField(max_length=10)


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    number_account = models.CharField(max_length=10, unique=True)
    agency = models.CharField(max_length=4)
    balance = models.DecimalField()

