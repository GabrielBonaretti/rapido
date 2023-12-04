from django.db import models

from card.models import Card

from account.models import Account

# Create your models here.

class Credit(models.Model):
    valueTotal = models.FloatField()
    numberTotalParcels = models.IntegerField()
    numberPayedParcels = models.IntegerField(default=0)
    observation = models.CharField(max_length=255, blank=True)
    credit_card = models.ForeignKey(Card, on_delete=models.DO_NOTHING)
    account_received = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True)


class CreditParcel(models.Model):
    number_parcel = models.IntegerField()
    value_parcel = models.FloatField()
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, default=None)
    credit = models.ForeignKey(Credit, on_delete=models.DO_NOTHING)
