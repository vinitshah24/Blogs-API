import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse
from django.utils import timezone

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    # Read-only fields are included in the API output,
    # but should not be included in the input during create or update operations
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    #token_response = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'password2', 'token', 'expires',  # 'token_response'
                  'message']
        # Ensure that the field may be used when updating or creating an instance,
        # but is not included when serializing the representation [Prevent Showing on GET]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Password Mismatch")
        return data

    def create(self, validated_data):
        # Overriding the create method because we have to save password differently
        # Default will just save User(username, email, password, password2)
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = False  # Does not log in directly after registering
        user_obj.save()
        return user_obj

    def get_token(self, obj):  # instance of the model
        user = obj
        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)
        return token

    def get_expires(self, obj):
        return timezone.now() + \
            api_settings.JWT_REFRESH_EXPIRATION_DELTA - \
            datetime.timedelta(seconds=200)

    # def get_token_response(self, user):
    #     payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    #     token = api_settings.JWT_ENCODE_HANDLER(payload)
    #     response = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(token, user, request=None)
    #     return response

    def get_message(self, obj):
        return "Registration Successful!"


# User details - nested serialization
class UserPublicSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'uri']

    def get_uri(self, obj):
        #return "/api/users/{id}/".format(id=obj.id)
        request = self.context.get('request')
        return api_reverse("api-user:detail", kwargs={"username": obj.username}, request=request)

class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    status_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'uri']

    def get_uri(self, obj):
        return "/api/users/{id}/".format(id=obj.id)

    def get_status_list(self, obj):
        return "obj"
