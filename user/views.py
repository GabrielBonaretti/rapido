from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status, generics

from rest_framework_simplejwt import authentication as authenticationJWT

from user.serializers import UserSerializer, AdressSerializer, AccountSerializer, AccountWithUserSerializer, TransactionSerializer
from rest_framework.decorators import action

from user.models import (
    User,
    Adress,
    Account,
    Transaction
)

import random
from datetime import datetime, timedelta, timezone

from rest_framework_simplejwt.tokens import AccessToken  # Import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate


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

            print(datetime.utcnow().isoformat() + 'Z')
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
            elif sender.balance <= 0:
                return Response(
                    {"detail": "You cannot transfer a negative amount or any amount!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            transaction = {
                "account_sent": 1,
                "account_received": received_id,
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
