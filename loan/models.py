from django.db import models

from account.models import Account

# Create your models here.

class Loan(models.Model):
    valueLoan = models.FloatField()
    numberTotalParcels = models.IntegerField()
    numberPayedParcels = models.IntegerField(default=0)
    observation = models.CharField(max_length=255)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)


class LoanParcel(models.Model):
    number_parcel = models.IntegerField()
    value_parcel = models.FloatField()
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, default=None)
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
