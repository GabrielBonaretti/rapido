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
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    url_image = models.ImageField(null=True, upload_to=user_image_field)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []