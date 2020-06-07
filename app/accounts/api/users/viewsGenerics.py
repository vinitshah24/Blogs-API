
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, pagination
from accounts.api.permissions import AnonPermissionOnly

from blogs.models import Blogs as BlogsModel
from blogs.api.serializers import BlogsInlineSerializer
from blogs.api.views import BlogsListView
from app.pagination import BlogsPagination
from .serializers import UserDetailSerializer

User = get_user_model()


class UserDetailAPIView(generics.RetrieveAPIView):
    #permission_classes  = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    lookup_field = 'username'  # id

    def get_serializer_context(self):
        return {'request': self.request}


class UserBlogsAPIView(generics.ListAPIView):
    serializer_class = BlogsInlineSerializer
    pagination_class = BlogsPagination

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username", None)
        if username is None:
            return BlogsModel.objects.none()
        return BlogsModel.objects.filter(user__username=username)
