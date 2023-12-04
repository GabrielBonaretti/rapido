from rest_framework import serializers
from adress.models import Adress
from user.models import User

class AdressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Add this line to specify the queryset
        many=False,
        write_only=True
    )

    class Meta:
        model = Adress
        fields = '__all__'
