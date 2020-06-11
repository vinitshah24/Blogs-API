from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from .views import AuthAPIView, RegisterAPIView

urlpatterns = [
    path('jwt/register/', RegisterAPIView.as_view(), name='register'),
    path('', AuthAPIView.as_view(), name='login'),  # Manual Token Generation
    # path('jwt/', obtain_jwt_token),  # Automatic Token Generation
    path('jwt/refresh/', refresh_jwt_token),
]
