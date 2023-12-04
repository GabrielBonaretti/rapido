import os
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from cpf_field import models as modelcpf


def user_image_field(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join('uploads', 'user', filename)


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    cpf = modelcpf.CPFField('cpf', unique=True, default='')
    url_image = models.ImageField(null=True, upload_to=user_image_field)
    password = models.CharField(max_length=255)
    declared_salary = models.FloatField(default=0.00, null=True)
    last_try_login = models.DateTimeField(default=datetime.now)
    count_try_login = models.IntegerField(default=0)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = []
