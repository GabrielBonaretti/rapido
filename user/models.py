import os
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

def user_image_field(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join('uploads', 'user', filename)


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    url_image = models.ImageField(null=True, upload_to=user_image_field)
    password = models.CharField(max_length=255)
    declared_salary = models.FloatField(default=0)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Adress(models.Model):
    state = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    city = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    cep = models.CharField(max_length=8)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Account(models.Model):
    number_account = models.CharField(max_length=10, unique=True)
    agency = models.CharField(max_length=4)
    balance = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class TypeTransaction(models.Model):
    type_transaction = models.CharField(max_length=255)


class Transaction(models.Model):
    value = models.FloatField(default=0)
    description = models.CharField(max_length=255)
    account_sent = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="account_sent")
    account_received = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="account_received", null=True)
    type_transaction = models.ForeignKey(TypeTransaction, on_delete=models.DO_NOTHING, null=True)
    
    
class TypeCard(models.Model):
    type_card = models.CharField(max_length=255)
    
    
class Card(models.Model):
    number = models.CharField(max_length=20)
    cvv = models.CharField(max_length=3)
    due_data = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=True)    
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type_card = models.ForeignKey(TypeCard, on_delete=models.DO_NOTHING)


class Credit(models.Model):
    valueTotal = models.FloatField()
    fees = models.DecimalField(max_digits=5, decimal_places=4)
    numberTotalParcels = models.IntegerField()
    approved = models.BooleanField(default=True)
    observation = models.CharField(max_length=255)
    credit_card = models.ForeignKey(Card, on_delete=models.DO_NOTHING)
    
    
class CreditParcel(models.Model):
    numberParcels = models.IntegerField()
    value_parcel = models.FloatField()
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    value_paid = models.FloatField()
    paid_date = models.DateField(auto_now=False, auto_now_add=False)
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
    value_paid = models.FloatField()
    paid_date = models.DateField(auto_now=False, auto_now_add=False)
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING)