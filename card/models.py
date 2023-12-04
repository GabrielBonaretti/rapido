from django.db import models

from user.models import User

# Create your models here.

class Card(models.Model):
    number = models.CharField(max_length=20)
    cvv = models.CharField(max_length=3)
    due_data = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type_card = models.CharField(max_length=50)
