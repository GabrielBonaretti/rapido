from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status, generics

from rest_framework_simplejwt import authentication as authenticationJWT

from user.serializers import UserSerializer, AdressSerializer
from rest_framework.decorators import action

from user.models import (
    Adress
)

   
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
        user_serializer = self.serializer_class(data=request.data)  # Save the user and get the instance
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        print(user.id)
        adress = {
            "state": "",
            "uf": "",
            "city": "",
            "neighborhood": "",
            "street": "",
            "number": 0,
            "cep": 0,
            "user": user.id
        }
        
        print(adress)
        adress_serializer = AdressSerializer(data=adress)
        adress_serializer.is_valid(raise_exception=True)
        adress_serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class AdressAPIView(viewsets.GenericViewSet):
    queryset = Adress.objects.all()
    serializer_class = AdressSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]


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
    

    @action(methods=['PUT'], detail=False, url_path="search")
    def put_adress_by_user(self, resquest):
        try:
            user = self.get_object()
            adress_upload = resquest.data
            adress = self.queryset.filter(user=int(user.pk)).first()
            serializer = self.serializer_class(adress, adress_upload)

            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
