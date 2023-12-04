from django.db import models
from user.models import User

# Create your models here.

class Account(models.Model):
    number_account = models.CharField(max_length=10, unique=True)
    agency = models.CharField(max_length=4)
    balance = models.FloatField(default=0.00)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)