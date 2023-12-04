from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics

from rest_framework_simplejwt import authentication as authenticationJWT
from rest_framework_simplejwt.tokens import AccessToken  # Import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema

from django.contrib.auth import authenticate
from django.utils import timezone

from user.models import User
from user.serializers import UserSerializer

from adress.serializers import AdressSerializer

from account.serializers import AccountSerializer

from card.serializers import CardSerializer

import random

from datetime import datetime, timedelta

@extend_schema(tags=['User'])
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


@extend_schema(tags=['User'])
class ManagerUserAPIView(generics.RetrieveUpdateAPIView):
    """Manage for the users"""
    serializer_class = UserSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user


@extend_schema(tags=['User'])
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