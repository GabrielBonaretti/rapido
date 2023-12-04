from rest_framework import serializers

from user.models import User
from user.serializers import UserPublicSerializer, UserForTransactionSerializer

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Add this line to specify the queryset
        many=False
    )

    class Meta:
        model = Account
        fields = '__all__'


class AccountWithUserSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer()

    class Meta:
        model = Account
        fields = ["id", "user", "number_account", "agency"]

class AccountForTransactionSerialzier(serializers.ModelSerializer):
    user = UserForTransactionSerializer()

    class Meta:
        model = Account
        fields = ["user"]