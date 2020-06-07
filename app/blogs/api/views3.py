import json
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from blogs.models import Blogs as BlogsModel
from .serializers import BlogsSerializer
from .utils import is_valid_json

# ListModelMixin     - GET LIST
# RetrieveModelMixin - GET SINGLE ITEM
# CreateModelMixin   - POST
# UpdateModelMixin   - PUT
# DestroyModelMixin  - DELETE

class BlogsAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                   generics.ListAPIView):
    
    permission_classes = []
    authentication_classes = []
    serializer_class = BlogsSerializer
    passed_id = None

    # Returns the queryset that should be used for list views,
    # and that should be used as the base for lookups in detail views
    # IF ?q=X is present, it filters the content or else returns full list
    def get_queryset(self):
        request = self.request
        qs = BlogsModel.objects.all()
        query = request.GET.get('q')
        if query is not None:
            # (NAME_icontains) case-insensitive match for blog content
            qs = qs.filter(content__icontains=query)
        return qs

    # Returns an object instance that should be used for detail views
    def get_object(self):
        request = self.request
        passed_id = request.GET.get('id', None) or self.passed_id
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    # perform_destroy(self, instance) - Called by DestroyModelMixin when deleting object instance
    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None

    def get(self, request, *args, **kwargs):
        url_passed_id = request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_valid_json(body_):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        # print(request.body)
        # print(request.data)
        passed_id = url_passed_id or new_passed_id or None
        self.passed_id = passed_id
        if passed_id is not None:  # or passed_id is not "":
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        url_passed_id = request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_valid_json(body_):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        passed_id = url_passed_id or new_passed_id or None
        self.passed_id = passed_id
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.put(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        url_passed_id = request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_valid_json(body_):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        passed_id = url_passed_id or new_passed_id or None
        self.passed_id = passed_id
        return self.destroy(request, *args, **kwargs)

"""
from django.urls import path

from .views import BlogsAPIView

urlpatterns = [
    path('', BlogsAPIView.as_view()),
]
"""
