import datetime

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from .serializers import RegisterSerializer
from rest_framework import generics, status


class RegisterView(generics.CreateAPIView):
    """Registration view"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    """Login view"""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            serializer.user.last_login = datetime.datetime.now()
            serializer.user.save()
        return response
