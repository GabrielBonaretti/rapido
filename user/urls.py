from django.urls import path
from user import views

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('user/', views.ManagerUserAPIView.as_view(), name='user'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
]
