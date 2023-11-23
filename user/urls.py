from django.urls import path, include
from user import views


from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('adress', views.AdressAPIView)
router.register('account', views.AccountAPIView)
router.register('transaction', views.TransactionAPIView)

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('user/', views.ManagerUserAPIView.as_view(), name='user'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    # path('transaction/', views.TransactionAPIView.as_view(), name='transaction'),

    path('', include(router.urls))
]
