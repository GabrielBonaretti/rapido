from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from account.models import Account
from account.serializers import AccountSerializer, AccountWithUserSerializer

from user.models import User

# Create your views here.

@extend_schema(tags=['Account'])
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
