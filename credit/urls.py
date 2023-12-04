from django.urls import path, include
from credit import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('credit', views.CreditAPIView)
router.register('parcelsCredit', views.CreditParcelAPIView)

urlpatterns = [
    path('', include(router.urls))
]
