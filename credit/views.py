from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from django.utils import timezone

from dateutil.relativedelta import relativedelta

from credit.models import Credit, CreditParcel
from credit.serializers import CreditSerializer, CreditParcelSerializer, CreditGetSerializer

from card.models import Card

from transaction.serializers import TransactionSerializer

from account.models import Account

# Create your views here.


class CreditAPIView(viewsets.GenericViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    def create(self, request):
        user = self.get_object()

        valueTotal = request.data.get('valueTotal')
        numberTotalParcels = request.data.get('numberTotalParcels')
        observation = request.data.get('observation')
        receiver_id = request.data.get('account_received')

        card = Card.objects.filter(user=int(user.id)).filter(
            type_card="Credit").filter(active=True).first()

        if card is None:
            return Response(
                {"detail": "You do not have a credit card to make this transaction!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        credit = {
            "valueTotal": valueTotal,
            "numberTotalParcels": numberTotalParcels,
            "observation": observation,
            "credit_card": card.id,
            "account_received": receiver_id
        }

        serializer = self.get_serializer(data=credit)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        credit = Credit.objects.latest("id")
        parcelValue = valueTotal / numberTotalParcels
        for i in range(numberTotalParcels):
            current_date = timezone.localdate()
            new_date = current_date + relativedelta(months=(i+1))

            creditParcel = {
                "number_parcel": i+1,
                "value_parcel": parcelValue,
                "due_date": new_date.replace(day=15),
                "credit": credit.id
            }

            serializer_parcel = CreditParcelSerializer(data=creditParcel)
            serializer_parcel.is_valid(raise_exception=True)
            serializer_parcel.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        user = self.get_object()
        card = Card.objects.filter(user=int(user.id)).filter(
            type_card="Credit").filter(active=True).first()

        if not card:
            return Response(
                {"detail": "You do not have a credit card!"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        credit = Credit.objects.filter(credit_card=card.id).all()
        serializer = CreditGetSerializer(credit, many=True)
        return Response(serializer.data)


class CreditParcelAPIView(viewsets.GenericViewSet):
    queryset = CreditParcel.objects.all()
    serializer_class = CreditParcelSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    @action(methods=['GET'], detail=True, url_path="all")
    def get_parcel_by_credit(self, request, pk=None):
        user = self.get_object()
        card = Card.objects.filter(user=int(user.id)).filter(
            type_card="Credit").filter(active=True).first()
        credit = Credit.objects.filter(credit_card=card.id).filter(id=pk)

        if not credit:
            return Response(
                {"detail": "Something was wrong"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        queryset = CreditParcel.objects.filter(credit=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path="paid")
    def paid_credit_parcel(self, request, pk=None):
        user = self.get_object()
        card = Card.objects.filter(user=int(user.id)).filter(
            type_card="Credit").filter(active=True).first()
        parcel_credit = CreditParcel.objects.filter(id=pk).first()
        credit = Credit.objects.filter(id=parcel_credit.credit.id).filter(
            credit_card=card.id).first()

        if parcel_credit.paid:
            return Response(
                {"detail": "This parcel is already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif credit:
            transaction = {
                "account_sent": user.id,
                "account_received": credit.account_received.id,
                "card": card.id,
                "value": parcel_credit.value_parcel,
                "description": "Paid value credit parcel",
                "type_transaction": "Credit card"
            }

            transaction_serializer = TransactionSerializer(data=transaction)
            transaction_serializer.is_valid(raise_exception=True)
            transaction_serializer.save()

            sender = Account.objects.filter(id=user.id).first()
            sender.balance -= parcel_credit.value_parcel
            sender.save()

            received = Account.objects.filter(
                id=credit.account_received.id).first()
            received.balance += parcel_credit.value_parcel
            received.save()

            parcel_credit.paid = True
            parcel_credit.paid_date = timezone.localdate()
            parcel_credit.save()

            credit.numberPayedParcels += 1
            credit.save()
            return Response(
                {"detail": "You paid this parcel"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Something wrong happened"},
                status=status.HTTP_401_UNAUTHORIZED
            )
