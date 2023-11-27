from rest_framework import serializers
from user.models import (
    User,
    Adress,
    Account,
    Transaction
)

from datetime import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'cpf',
            'password',
            'declared_salary',
            'url_image'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        
        if password is not None:
            user.set_password(password)

        user.save()
        return user
    
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'cpf',
        ]    

class AdressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Add this line to specify the queryset
        many=False,
        write_only=True
    )

    class Meta:
        model = Adress
        fields = '__all__'


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

class TransactionSerializer(serializers.ModelSerializer):
    account_sent = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),  # Add this line to specify the queryset
        many=False,
        allow_null=True  # Allow null values for this field
    )

    account_received = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),  # Add this line to specify the queryset
        many=False,
        allow_null=True  # Allow null values for this field
    )

    class Meta:
        model = Transaction
        fields = '__all__'
    
    
class UserForTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]
        
class AccountForTransactionSerialzier(serializers.ModelSerializer):
    user = UserForTransactionSerializer()

    class Meta:
        model = Account
        fields = ["user"]

class TransactionGetSerializer(serializers.ModelSerializer):
    account_sent = AccountForTransactionSerialzier()
    account_received = AccountForTransactionSerialzier()

    class Meta:
        model = Transaction
        fields = '__all__'
    