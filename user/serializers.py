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
            'password',
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
        many=False,
        read_only=True
    )

    class Meta:
        model = Adress
        fields = [
            'id',
            'state',
            'uf',
            'city',
            'neighborhood',
            'street',
            'number',
            'cep',  
            'user'
        ]


# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = [
#             'id',
#             'name',
#             'email',
#             'password',
#             'url_image'
#         ]
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }