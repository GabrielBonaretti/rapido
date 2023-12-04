from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from adress.models import Adress
from adress.serializers import AdressSerializer

# Create your views here.

@extend_schema(tags=['Adress'])
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