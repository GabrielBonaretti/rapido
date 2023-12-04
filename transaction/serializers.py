from rest_framework import serializers

from account.models import Account
from account.serializers import AccountForTransactionSerialzier

from card.models import Card

from transaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    account_sent = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        many=False,
        allow_null=True
    )

    account_received = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        many=False,
        allow_null=True
    )

    card = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(),
        many=False,
        allow_null=True
    )

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionGetSerializer(serializers.ModelSerializer):
    account_sent = AccountForTransactionSerialzier()
    account_received = AccountForTransactionSerialzier()

    class Meta:
        model = Transaction
        fields = '__all__'
