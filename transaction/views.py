from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from django.db.models import Q

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer, TransactionGetSerializer

from account.models import Account

from card.models import Card

# Create your views here.

class TransactionAPIView(viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    def create(self, request):
        try:
            user = self.get_object()
            received_id = request.data.get('account_received')
            value = request.data.get('value')
            description = request.data.get('description')
            type_transaction = request.data.get('type_transaction')

            sender = Account.objects.filter(id=user.id).first()

            if sender.balance < value:
                return Response(
                    {"detail": "You do not have enough balance to make this transaction!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif value <= 0:
                return Response(
                    {"detail": "You cannot transfer a negative amount or any amount!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            transaction = {
                "account_sent": user.id,
                "account_received": received_id,
                "card": None,
                "value": value,
                "description": description,
                "type_transaction": type_transaction
            }

            transactio_serializer = TransactionSerializer(data=transaction)
            transactio_serializer.is_valid(raise_exception=True)
            transactio_serializer.save()

            sender.balance -= value
            sender.save()

            received = Account.objects.filter(id=received_id).first()
            received.balance += value
            received.save()

            return Response(status=status.HTTP_201_CREATED)

        except Exception as error:
            print(error)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['POST'], detail=False, url_path="debitcard")
    def create_with_card(self, request):
        try:
            user = self.get_object()
            received_id = request.data.get('account_received')
            value = request.data.get('value')
            description = request.data.get('description')
            type_transaction = request.data.get('type_transaction')

            sender = Account.objects.filter(id=user.id).first()
            card = Card.objects.filter(user=int(user.id)).filter(
                type_card="Debit").filter(active=True).first()

            if not card:
                return Response(
                    {"detail": "Don't find this card!"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if sender.balance < value:
                return Response(
                    {"detail": "You do not have enough balance to make this transaction!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif value <= 0:
                return Response(
                    {"detail": "You cannot transfer a negative amount or any amount!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            transaction = {
                "account_sent": user.id,
                "account_received": received_id,
                "card": card.id,
                "value": value,
                "description": description,
                "type_transaction": type_transaction
            }

            transaction_serializer = TransactionSerializer(data=transaction)
            transaction_serializer.is_valid(raise_exception=True)
            transaction_serializer.save()

            sender.balance -= value
            sender.save()

            received = Account.objects.filter(id=received_id).first()
            received.balance += value
            received.save()

            return Response(status=status.HTTP_201_CREATED)

        except Exception as error:
            print(error)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path="search")
    def get_all_transactions_related_me(self, request):
        paginator = LimitOffsetPagination()

        try:
            user = self.get_object()
            transactions = Transaction.objects.filter(
                Q(account_sent=user.id) | Q(account_received=user.id)).order_by('-create')

            paginated_queryset = paginator.paginate_queryset(
                transactions, request)

            serializer = TransactionGetSerializer(
                paginated_queryset, many=True)

            return paginator.get_paginated_response(serializer.data)
        except Exception as error:
            print(error)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['POST'], detail=False, url_path="receive")
    def post_receive_transaction(self, request):
        try:
            value = float(request.data.get('value'))

            if value <= 0:
                return Response(
                    {"detail": "This field may not be blank!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = self.get_object()

            transaction = {
                "account_sent": None,
                "account_received": user.id,
                "card": None,
                "value": value,
                "description": "Anonymous transaction made",
                "type_transaction": "Transfer"
            }

            transaction_serializer = TransactionSerializer(data=transaction)
            transaction_serializer.is_valid(raise_exception=True)
            transaction_serializer.save()

            received = Account.objects.filter(id=user.id).first()
            received.balance += value
            received.save()

            return Response(status=status.HTTP_201_CREATED)

        except Exception as error:
            print(error)
            return Response(status=status.HTTP_404_NOT_FOUND)
