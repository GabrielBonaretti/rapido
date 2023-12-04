from django.urls import path, include
from transaction import views

from rest_framework.routers import SimpleRouter, DefaultRouter

app_name = 'transaction'

router = DefaultRouter()
router.register('transaction', views.TransactionAPIView)

urlpatterns = [
    path('', include(router.urls))
]
