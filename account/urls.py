from django.urls import path, include
from account import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('account', views.AccountAPIView)

urlpatterns = [
    path('', include(router.urls))
]
