from django.urls import path
from user import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('user/', views.ManagerUserAPIView.as_view(), name='user'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
