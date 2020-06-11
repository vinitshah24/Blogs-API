from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import UserRegisterSerializer, UserDetailSerializer
from .permissions import AnonPermissionOnly, IsOwnerOrReadOnly

User = get_user_model()

# Custom Authentication Views - Creating a new token manually
class AuthAPIView(APIView):
    # permission_classes = [permissions.AllowAny]
    permission_classes = [AnonPermissionOnly]

    def post(self, request, *args, **kwargs):
        # print(request.user)
        if request.user.is_authenticated:
            return Response({'detail': 'Already authenticated!'}, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        qs = User.objects \
            .filter(Q(username__iexact=username) | Q(email__iexact=username)) \
            .distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                # Custom function to generate the token payload
                payload = api_settings.JWT_PAYLOAD_HANDLER(user)
                token = api_settings.JWT_ENCODE_HANDLER(payload)
                # Controlling the response data returned after login or refresh. 
                # Override to return a custom response - serialized representation of the User
                response = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(token, user, request=request)
                return Response(response)
        return Response({"detail": "Invalid credentials"}, status=401)


class RegisterAPIView(generics.CreateAPIView):
    # permission_classes = [permissions.AllowAny]
    permission_classes = [AnonPermissionOnly]
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    # Returns a dict containing any extra context that should be supplied to serializer
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
