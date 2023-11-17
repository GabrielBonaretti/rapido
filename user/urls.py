from django.urls import path, include
from user import views

from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('adress', views.AdressAPIView)

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('user/', views.ManagerUserAPIView.as_view(), name='user'),

    path('', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
