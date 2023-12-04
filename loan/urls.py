from django.urls import path, include
from loan import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('loan', views.LoanAPIView)
router.register('parcelsLoan', views.LoanParcelAPIView)

urlpatterns = [
    path('', include(router.urls))
]
