import json

from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication

from blogs.models import Blogs as BlogsModel
from .serializers import BlogsSerializer
from accounts.api.permissions import IsOwnerOrReadOnly

# ListModelMixin     - GET LIST
# RetrieveModelMixin - GET SINGLE ITEM
# CreateModelMixin   - POST
# UpdateModelMixin   - PUT
# DestroyModelMixin  - DELETE


class BlogsDetailView(mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      generics.RetrieveAPIView):

    #authentication_classes = []
    # [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BlogsSerializer
    queryset = BlogsModel.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BlogsListView(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, generics.ListAPIView):

    #authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BlogsSerializer
    passed_id = None
    # Filter
    search_fields = ('user__username', 'content', 'user__email')
    ordering_fields = ('user__username', 'timestamp')
    queryset = BlogsModel.objects.all()

    # def get_queryset(self):
    #     request = self.request
    #     qs = BlogsModel.objects.all()
    #     query = request.GET.get('q')
    #     if query is not None:
    #         qs = qs.filter(content__icontains=query)
    #     return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # Including the userID while Creating new Blog post
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
