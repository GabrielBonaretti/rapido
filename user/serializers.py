from rest_framework import serializers
from user.models import (
    User,
    Adress,
    Account
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
    

class AdressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Add this line to specify the queryset
        many=False,
        write_only=True
    )

    class Meta:
        model = Adress
        fields = [
            'id',
            'uf',
            'city',
            'neighborhood',
            'street',
            'number',
            'cep',  
            'user'
        ]


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Add this line to specify the queryset
        many=False,
        write_only=True
    )
    
    class Meta:
        model = Account
        fields = [
            'number_account',
            'agency',
            'balance',
            'user'
        ]