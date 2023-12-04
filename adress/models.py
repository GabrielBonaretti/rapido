from django.db import models
from user.models import User

# Create your models here.

class Adress(models.Model):
    uf = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=255, blank=True)
    neighborhood = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    number = models.IntegerField()
    cep = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')
