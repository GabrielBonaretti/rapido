from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from django.utils import timezone

from dateutil.relativedelta import relativedelta

from loan.models import Loan, LoanParcel
from loan.serializers import LoanSerializer, LoanParcelSerializer

from account.models import Account

from transaction.serializers import TransactionSerializer

# Create your views here.

class LoanAPIView(viewsets.GenericViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    def create(self, request):
        user = self.get_object()
        account = Account.objects.filter(user=user.id).first()

        value_loan = request.data.get('valueLoan')
        number_total_parcels = request.data.get('numberTotalParcels')
        observation = request.data.get('observation')

        value_parcel = (value_loan / number_total_parcels) * 1.05

        print(user.declared_salary * 0.4)
        print(value_parcel)
        if not user.declared_salary * 5 >= value_loan or not user.declared_salary * 0.4 >= value_parcel:
            return Response(
                {"detail": "Your loan request was not approved."},
                status=status.HTTP_201_CREATED
            )

        transaction = {
            "account_sent": None,
            "account_received": user.id,
            "card": None,
            "value": value_loan,
            "description": "Loan received",
            "type_transaction": "Loan"
        }

        transaction_serializer = TransactionSerializer(data=transaction)
        transaction_serializer.is_valid(raise_exception=True)
        transaction_serializer.save()

        account.balance += value_loan
        account.save()

        loan = {
            "account": account.id,
            "valueLoan": value_loan,
            "numberTotalParcels": number_total_parcels,
            "observation": observation
        }

        serializer = self.get_serializer(data=loan)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        loan_object = Loan.objects.latest("id")
        for i in range(number_total_parcels):
            current_date = timezone.localdate()
            new_date = current_date + relativedelta(months=(i+1))

            loan_parcel = {
                "number_parcel": i+1,
                "value_parcel": value_parcel,
                "due_date": new_date.replace(day=15),
                "loan": loan_object.id
            }

            serializer_parcel = LoanParcelSerializer(data=loan_parcel)
            serializer_parcel.is_valid(raise_exception=True)
            serializer_parcel.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        user = self.get_object()
        account = Account.objects.filter(user=user.id).first()
        loan = Loan.objects.filter(account=account.id).all()
        serializer = LoanSerializer(loan, many=True)
        return Response(serializer.data)

class LoanParcelAPIView(viewsets.GenericViewSet):
    queryset = LoanParcel.objects.all()
    serializer_class = LoanParcelSerializer

    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user

    @action(methods=['GET'], detail=True, url_path="all")
    def get_parcel_by_loan(self, request, pk=None):
        user = self.get_object()
        account = Account.objects.filter(user=user.id).first()
        loan = Loan.objects.filter(account=account.id).filter(id=pk).first()
        
        if not loan:
            return Response(
                {"detail": "Something was wrong"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        queryset = LoanParcel.objects.filter(loan=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path="paid")
    def paid_loan_parcel(self, request, pk=None):
        user = self.get_object()
        account = Account.objects.filter(user=user.id).first()
        parcel_loan = LoanParcel.objects.filter(id=pk).first()
        loan = Loan.objects.filter(id=parcel_loan.loan.id).first()

        if account.id != loan.account.id:
            return Response(
                {"detail": "Something was wrong"},
                status=status.HTTP_401_UNAUTHORIZED
            )  
        
        if parcel_loan.paid:
            return Response(
                {"detail": "This parcel is already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            transaction = {
                "account_sent": user.id,
                "account_received": None,
                "card": None,
                "value": parcel_loan.value_parcel,
                "description": "Paid value loan parcel",
                "type_transaction": "Loan"
            }

            transaction_serializer = TransactionSerializer(data=transaction)
            transaction_serializer.is_valid(raise_exception=True)
            transaction_serializer.save()

            sender = Account.objects.filter(id=user.id).first()
            sender.balance -= parcel_loan.value_parcel
            sender.save()


            parcel_loan.paid = True
            parcel_loan.paid_date = timezone.localdate()
            parcel_loan.save()

            loan.numberPayedParcels += 1
            loan.save()
            
            return Response(
                {"detail": "You paid this parcel"},
                status=status.HTTP_200_OK
            )