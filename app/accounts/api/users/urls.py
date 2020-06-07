from django.contrib import admin
from django.urls import path, include

from .views import UserDetailAPIView, UserBlogsAPIView

urlpatterns = [
    path('<username>', UserDetailAPIView.as_view(), name='detail'),
    path('<username>/blogs/', UserBlogsAPIView.as_view(), name='blogs-list'),
]
