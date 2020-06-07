from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from blogs.models import Blogs as BlogsModel

from accounts.api.serializers import UserPublicSerializer

# Serializers -> To convert querysets to JSON, validate data


class BlogsSerializer(serializers.ModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = BlogsModel
        fields = ['id', 'user', 'content', 'image', 'uri']
        read_only_fields = ['user']  # GET

    # def validate_content(self, value):
    #     if len(value) > 10000:
    #         raise serializers.ValidationError("Content Field too Large")
    #     return value

    def validate(self, data):
        content = data.get("content", None)
        if content == "":
            content = None
        image = data.get("image", None)
        if content is None and image is None:
            raise serializers.ValidationError("Content or Image Required!")
        return data

    def get_uri(self, obj):
        #return "/api/status/{id}/".format(id=obj.id)
        request = self.context.get('request')
        return api_reverse('api-blogs:details', kwargs={"id": obj.id}, request=request)

# class BlogsInlineSerializer(serializers.ModelSerializer):
#     uri = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = BlogsModel
#         fields = ['id', 'content', 'image', 'uri']

#     def get_uri(self, obj):
#         return "/api/status/{id}/".format(id=obj.id)

class BlogsInlineSerializer(BlogsSerializer):
    class Meta:
        model = BlogsModel
        fields = ['id', 'content', 'image', 'uri']
        
        