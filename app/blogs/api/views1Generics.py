from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from blogs.models import Blogs as BlogsModel
from .serializers import BlogsSerializer


class BlogsListSearchAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        qs = BlogsModel.objects.all()
        serializer = BlogsSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # { "post": { "user": 1, "content": "Hello!", "image": null } }
        blog_post = request.data.get('post')
        serializer = BlogsSerializer(data=blog_post)
        if serializer.is_valid(raise_exception=True):
            blog_saved = serializer.save()
        return Response({"success": "Blog '{}' created successfully!".format(blog_saved.content)})


class BlogsAPIView(generics.ListAPIView):
    # GET - Used for read-only endpoints to represent a collection of model instances
    permission_classes = []
    authentication_classes = []
    serializer_class = BlogsSerializer

    def get_queryset(self):
        qs = BlogsModel.objects.all()
        # Filter the word passed in the query
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs


class BlogsCreateAPIView(generics.CreateAPIView):
    # POST
    permission_classes = []
    authentication_classes = []
    queryset = BlogsModel.objects.all()
    serializer_class = BlogsSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class BlogsDetailAPIView(generics.RetrieveAPIView):
    # GET - Used for read-only endpoints to represent a single model instance
    permission_classes = []
    authentication_classes = []
    queryset = BlogsModel.objects.all()
    serializer_class = BlogsSerializer
    # lookup_field = 'id'
    # def get_object(self, *args, **kwargs):
    #     kwargs = self.kwargs
    #     kw_id = kwargs.get('abc')
    #     return BlogsModel.objects.get(id=kw_id)


class BlogsUpdateAPIView(generics.UpdateAPIView):
    # PUT and PATCH - Used for update-only endpoints for a single model instance
    permission_classes = []
    authentication_classes = []
    queryset = BlogsModel.objects.all()
    serializer_class = BlogsSerializer


class BlogsDeleteAPIView(generics.DestroyAPIView):
    # DELETE
    permission_classes = []
    authentication_classes = []
    queryset = BlogsModel.objects.all()
    serializer_class = BlogsSerializer


"""
from django.urls import path

from .views import (
    BlogsListSearchAPIView,
    BlogsAPIView,
    BlogsCreateAPIView,
    BlogsDetailAPIView,
    BlogsUpdateAPIView,
    BlogsDeleteAPIView,
)

urlpatterns = [
    #path('', BlogsListSearchAPIView.as_view()),
    # /api/blogs/ -> List
    path('', BlogsAPIView.as_view()),
    # /api/blogs/create -> Create
    path('create', BlogsCreateAPIView.as_view()),
    # /api/blogs/12/ -> Detail
    path('<pk>', BlogsDetailAPIView.as_view()),
    # /api/blogs/12/update/ -> Update
    path('<pk>/update', BlogsUpdateAPIView.as_view()),
    # /api/blogs/12/delete/ -> Delete
    path('<pk>/delete', BlogsDeleteAPIView.as_view()),
]
"""
