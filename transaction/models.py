from django.db import models
from datetime import datetime

from account.models import Account

from card.models import Card

# Create your models here.

class Transaction(models.Model):
    value = models.FloatField(default=0)
    description = models.CharField(max_length=255, blank=True)
    account_sent = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        related_name="account_sent",
        null=True,
        default=None
    )

    account_received = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        related_name="account_received",
        null=True
    )
    create = models.DateTimeField(default=datetime.now)
    type_transaction = models.CharField(max_length=255)
    card = models.ForeignKey(
        Card,
        on_delete=models.DO_NOTHING,
        related_name="card",
        null=True,
        default=None
    )