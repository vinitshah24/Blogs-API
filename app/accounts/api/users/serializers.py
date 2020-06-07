import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from blogs.api.serializers import BlogsInlineSerializer

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'uri', 'status']

    def get_uri(self, obj):
        # return "/api/users/{id}/".format(id=obj.id)
        request = self.context.get('request')
        return api_reverse("api-user:detail", kwargs={"username": obj.username}, request=request)

    def get_status(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass
        qs = obj.status_set.all().order_by("-timestamp")  # [:10]
        data = {
            'uri': self.get_uri(obj) + "status/",
            # 'last': BlogsInlineSerializer(qs.first()).data,
            # 'recent': BlogsInlineSerializer(qs[:limit], many=True).data
            'last': BlogsInlineSerializer(
                qs.first(), context={'request': request}
            ).data,
            'recent': BlogsInlineSerializer(
                qs[:limit], many=True, context={'request': request}
            ).data
        }
        return data
