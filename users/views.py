from django.contrib.auth.models import User
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import UserActivity
from .serializers import RegisterSerializer, UserActivitySerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    """
    Registration view
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserActivityView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    User's last login & last activity view set

        user-activity-list: queryset
        user-activity-detail: object
    """
    queryset = UserActivity.objects.all().select_related('username').order_by('id')
    serializer_class = UserActivitySerializer
    permission_classes = [AllowAny]
