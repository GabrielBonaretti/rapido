from django.urls import path, include
from adress import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('adress', views.AdressAPIView)

urlpatterns = [
    path('', include(router.urls))
]
