from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status, generics, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from rest_framework_simplejwt import authentication as authenticationJWT
from rest_framework_simplejwt.tokens import AccessToken  # Import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils import timezone

from user.serializers import (
    UserSerializer,
    AdressSerializer,
    AccountSerializer,
    AccountWithUserSerializer,
    TransactionSerializer,
    TransactionGetSerializer,
    CardSerializer,
    CreditSerializer,
    CreditParcelSerializer
)

from user.models import (
    User,
    Adress,
    Account,
    Transaction,
    Card,
    Credit,
    CreditParcel
)

import random

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        cpf = request.data.get('cpf')
        password = request.data.get('password')

        if not cpf or not password:
            return Response(
                {"error": "Cpf or password cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(cpf=cpf).first()

        default_format_date = '%Y-%m-%d %H:%M:%S'
        now_try_string = datetime.strftime(datetime.now(), default_format_date)

        if user is None:
            return Response(
                {"detail": "No active account found with the given credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        last_try_string = datetime.strftime(
            user.last_try_login, default_format_date)
        difference = (datetime.strptime(now_try_string, default_format_date) -
                      datetime.strptime(last_try_string, default_format_date))

        if user.count_try_login == 2:
            if timedelta(minutes=1) - difference <= timedelta(seconds=0):
                user.count_try_login = 0
                user.save()
            else:
                return Response(
                    {"detail": f"You have tried to log in many times, try again {timedelta(minutes=1) - difference} minutes later"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        # Authenticate user
        user_auth = authenticate(request, username=cpf, password=password)

        if user_auth is None:
            if difference < timedelta(minutes=1) and user.count_try_login < 2:
                user.count_try_login += 1
            else:
                user.count_try_login = 0

            user.last_try_login = datetime.now()

            user.save()
            return Response(
                {"detail": "No active account found with the given credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user.save()
        # Generate JWT token
        access_token = AccessToken.for_user(user)
        token_data = {
            "access": str(access_token),
        }
        return Response(token_data, status=status.HTTP_200_OK)


class ManagerUserAPIView(generics.RetrieveUpdateAPIView):
    """Manage for the users"""
    serializer_class = UserSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        user_serializer = self.serializer_class(
            data=request.data)  # Save the user and get the instance
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        adress = {
            "uf": "",
            "city": "",
            "neighborhood": "",
            "street": "",
            "number": 0,
            "cep": 0,
            "user": user.id
        }

        adress_serializer = AdressSerializer(data=adress)
        adress_serializer.is_valid(raise_exception=True)
        adress_serializer.save()

        number_account = ""
        for n in range(10):
            if n == 8:
                number_account += '-'
            else:
                number_account += str(random.randint(0, 9))

        account = {
            "number_account": number_account,
            "agency": "0001",
            "balance": 0,
            "user": user.id
        }

        account_serializer = AccountSerializer(data=account)
        account_serializer.is_valid(raise_exception=True)
        account_serializer.save()

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
            "type_card": "Debit"
        }

        card_serializer = CardSerializer(data=card)
        card_serializer.is_valid(raise_exception=True)
        card_serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class AdressAPIView(viewsets.GenericViewSet):
    queryset = Adress.objects.all()
    serializer_class = AdressSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    @action(methods=['GET'], detail=False, url_path="search")
    def get_adress_by_user(self, request):
        try:
            user = self.get_object()
            adress = self.queryset.filter(user=int(user.pk)).first()
            serializer = self.serializer_class(adress)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['PUT'], detail=True, url_path="search")
    def put_adress_by_user(self, resquest, pk=None):
        try:
            user = self.get_object()
            adress = self.queryset.filter(user=int(user.pk)).first()
            adress_upload = resquest.data
            adress_upload['user'] = int(user.pk)
            serializer = self.serializer_class(adress, data=adress_upload)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        except Exception as error:
            print(error)
            return Response(status=status.HTTP_404_NOT_FOUND)


class AccountAPIView(viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    @action(methods=['GET'], detail=False, url_path="me")
    def get_account_by_user(self, request):
        try:
            user = self.get_object()
            account = self.queryset.filter(user=int(user.pk)).first()
            serializer = self.serializer_class(account)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path="search")
    def get_account_by_content(self, request):
        try:
            param_value = request.query_params.get('search')

            if not param_value:
                return Response(
                    {"detail": "This field may not be blank!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for i in range(4):
                if i == 0:
                    queryset_users = User.objects.filter(
                        name=param_value).first()
                    if queryset_users:
                        queryset_account = Account.objects.filter(
                            id=queryset_users.id).first()
                        break
                elif i == 1:
                    queryset_users = User.objects.filter(
                        email=param_value).first()
                    if queryset_users:
                        queryset_account = Account.objects.filter(
                            id=queryset_users.id).first()
                        break
                elif i == 2:
                    queryset_users = User.objects.filter(
                        cpf=param_value).first()
                    if queryset_users:
                        queryset_account = Account.objects.filter(
                            id=queryset_users.id).first()
                        break
                elif i == 3:
                    queryset_account = Account.objects.filter(
                        number_account=param_value).first()
                    if queryset_account:
                        break

            serializer = AccountWithUserSerializer(queryset_account)

            return Response(serializer.data)

        except Exception as error:
            print(error)
            return Response({"detail": "User do not find!"}, status=status.HTTP_404_NOT_FOUND)


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
    def create_new_credit_card(self, request):
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
            "credit_card": card.id
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


class CreditParcelAPIView(viewsets.GenericViewSet):
    queryset = CreditParcel.objects.all()
    serializer_class = CreditParcelSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    @action(methods=['GET'], detail=True, url_path="all")
    def get_parcel_by_redit(self, request, pk=None):
        user = self.get_object()
        card = Card.objects.filter(user=int(user.id)).filter(
            type_card="Credit").filter(active=True).first()
        credit = Credit.objects.filter(credit_card=card.id).filter(id=pk)

        if not credit:
            return Response(
                {"detail": "No active account found with the given credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        queryset = CreditParcel.objects.filter(credit=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
