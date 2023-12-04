from rest_framework import serializers

from card.models import Card

from user.models import User


class CardSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Add this line to specify the queryset
        many=False
    )

    class Meta:
        model = Card
        fields = '__all__'