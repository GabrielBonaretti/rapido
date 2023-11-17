from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import (
    status,
    generics,
)

from rest_framework_simplejwt import authentication as authenticationJWT

from user.serializers import UserSerializer
from rest_framework.decorators import action


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
class ManagerUserAPIView(generics.RetrieveUpdateAPIView):
    """Manage for the users"""
    serializer_class = UserSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    
    def get_object(self):
        """Retrieve and return a user."""
        return self.request.user
    
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
