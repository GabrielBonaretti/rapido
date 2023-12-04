from rest_framework import serializers

from account.models import Account

from loan.models import Loan
from loan.models import LoanParcel

class LoanSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        many=False
    )
    
    class Meta:
        model = Loan
        fields = '__all__'


class LoanParcelSerializer(serializers.ModelSerializer):
    loan = serializers.PrimaryKeyRelatedField(
        queryset=Loan.objects.all(),
        many=False
    )
    
    class Meta:
        model = LoanParcel
        fields = '__all__'