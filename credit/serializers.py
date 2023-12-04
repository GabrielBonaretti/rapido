from rest_framework import serializers

from card.models import Card

from account.models import Account
from account.serializers import AccountForTransactionSerialzier

from credit.models import Credit, CreditParcel

class CreditSerializer(serializers.ModelSerializer):
    credit_card = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(),  # Add this line to specify the queryset
        many=False
    )

    account_received = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),  # Add this line to specify the queryset
        many=False
    )

    class Meta:
        model = Credit
        fields = '__all__'


class CreditGetSerializer(serializers.ModelSerializer):
    credit_card = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(),  # Add this line to specify the queryset
        many=False
    )

    account_received = AccountForTransactionSerialzier()

    class Meta:
        model = Credit
        fields = '__all__'


class CreditParcelSerializer(serializers.ModelSerializer):
    credit = serializers.PrimaryKeyRelatedField(
        queryset=Credit.objects.all(),  # Add this line to specify the queryset
        many=False
    )

    class Meta:
        model = CreditParcel
        fields = '__all__'
