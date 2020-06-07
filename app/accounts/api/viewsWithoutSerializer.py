from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings


User = get_user_model()

# Custom Authentication Views
class AuthAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # print(request.user)
        if request.user.is_authenticated():
            return Response({'detail': 'You are already authenticated'}, status=400)
        data = request.data
        username = data.get('username')  # username or email address
        password = data.get('password')
        qs = User.objects \
            .filter(Q(username__iexact=username) | Q(email__iexact=username)) \
            .distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = api_settings.JWT_PAYLOAD_HANDLER(user)
                token = api_settings.JWT_ENCODE_HANDLER(payload)
                response = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(
                    token, user, request=request)
                return Response(response)
        return Response({"detail": "Invalid credentials"}, status=401)


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'Already Registered & Authenticated!'}, status=400)
        data = request.data
        username = data.get('username')
        email = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        qs = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        )
        if password != password2:
            return Response({"password": "Password failed to match!"}, status=401)
        if qs.exists():
            return Response({"detail": "Account already exists!"}, status=401)
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            return Response({'detail': "Successfully Registered!"}, status=201)
        return Response({"detail": "Invalid Request"}, status=400)

"""
EXAMPLE REGISTER:
{
   "username":"vinit",
   "password":"vinit",
   "password2":"vinit"
}
"""
