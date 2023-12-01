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


class Adress(models.Model):
    uf = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=255, blank=True)
    neighborhood = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    number = models.IntegerField()
    cep = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='user')


class Account(models.Model):
    number_account = models.CharField(max_length=10, unique=True)
    agency = models.CharField(max_length=4)
    balance = models.FloatField(default=0.00)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Card(models.Model):
    number = models.CharField(max_length=20)
    cvv = models.CharField(max_length=3)
    due_data = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type_card = models.CharField(max_length=50)


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


class Credit(models.Model):
    valueTotal = models.FloatField()
    numberTotalParcels = models.IntegerField()
    numberPayedParcels = models.IntegerField(default=0)
    observation = models.CharField(max_length=255, blank=True)
    credit_card = models.ForeignKey(Card, on_delete=models.DO_NOTHING)


class CreditParcel(models.Model):
    number_parcel = models.IntegerField()
    value_parcel = models.FloatField()
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, default=None)
    credit = models.ForeignKey(Credit, on_delete=models.DO_NOTHING)


class Loan(models.Model):
    valueLoan = models.FloatField()
    fees = models.DecimalField(max_digits=5, decimal_places=4)
    numberTotalParcels = models.IntegerField()
    approved = models.BooleanField(default=True)
    observation = models.CharField(max_length=255)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)


class LoanParcel(models.Model):
    numberParcels = models.IntegerField()
    value_parcel = models.FloatField()
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(
        auto_now=False, auto_now_add=False, default=None)
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)
