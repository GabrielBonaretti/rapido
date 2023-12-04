from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from django.utils import timezone

from card.models import Card
from card.serializers import CardSerializer

from transaction.models import Transaction

import random

# Create your views here.


class CardAPIView(viewsets.GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    def list(self, request):
        user = self.get_object()
        cards = self.queryset.filter(
            user=int(user.id)).filter(active=True).all()
        serializer = self.serializer_class(cards, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path="transactions")
    def list_transactions_by_card(self, request, pk: int = None):
        paginator = LimitOffsetPagination()

        user = self.get_object()
        card = self.queryset.filter(user=int(user.id)).filter(
            id=pk).filter(active=True)

        if not card:
            return Response(status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(
            card=pk).all().order_by('-create')
        paginated_queryset = paginator.paginate_queryset(
            transactions, request)

        serializer = TransactionGetSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=True, url_path="block")
    def block_card(self, request, pk: int = None):
        user = self.get_object()
        card = self.queryset.filter(user=int(user.id)).filter(id=pk).first()

        if not card:
            return Response(status=status.HTTP_404_NOT_FOUND)

        card.active = False
        card.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path="new")
    def create_new_card(self, request):
        user = self.get_object()
        type_card = request.data.get('type_card')

        if type_card == "Credit" and user.declared_salary < 1000:
            return Response(
                {"detail": "You do not have the necessary requirements to apply for a credit card!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        card = self.queryset.filter(user=int(user.id)).filter(
            type_card=type_card).filter(active=True).first()

        if card:
            return Response(
                {"detail": "You already have one " +
                    type_card.lower() + " card active!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        number = ""
        for n in range(19):
            if n == 4 or n == 9 or n == 14:
                number += ' '
            else:
                number += str(random.randint(0, 9))

        cvv = ""
        for n in range(3):
            cvv += str(random.randint(0, 9))

        card = {
            "user": user.id,
            "number": number,
            "cvv": cvv,
            "due_data": timezone.localdate() + timezone.timedelta(days=3650),
            "active": True,
            "type_card": type_card
        }

        card_serializer = CardSerializer(data=card)
        card_serializer.is_valid(raise_exception=True)
        card_serializer.save()

        return Response(status=status.HTTP_200_OK)
