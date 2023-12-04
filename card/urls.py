from django.urls import path, include
from card import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('card', views.CardAPIView)

urlpatterns = [
    path('', include(router.urls))
]
