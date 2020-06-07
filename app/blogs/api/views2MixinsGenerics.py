from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from blogs.models import Blogs as BlogsModel
from .serializers import BlogsSerializer

# CreateModelMixin - POST method - implements creating and saving a new model instance
# ListAPIView - Used for read-only endpoints to represent a collection of model instances
# http://127.0.0.1:8000/api/blogs/?q=wagwan
# http://127.0.0.1:8000/api/blogs/
class BlogsListView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = BlogsSerializer

    def get_queryset(self):
        qs = BlogsModel.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# UpdateModelMixin  - PUT method - implements updating and saving an existing model instance
# DestroyModelMixin - DELETE method - implements deletion of an existing model instance
# RetrieveAPIView - Used for read-only endpoints to represent a single model instance
# http://127.0.0.1:8000/api/blogs/2 -> Can be retrieved. modified, and deleted
class BlogsDetailView(mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                      generics.RetrieveAPIView):

    permission_classes = []
    authentication_classes = []
    queryset = BlogsModel.objects.all()
    serializer_class = BlogsSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


"""
from django.urls import path

from .views import (
    BlogsListView,
    BlogsDetailView,
)

urlpatterns = [
    path('', BlogsListView.as_view()),
    path('<pk>', BlogsDetailView.as_view()),
]
"""
