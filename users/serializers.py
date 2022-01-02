from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from users.models import UserActivity


class RegisterSerializer(serializers.ModelSerializer):
    """Registration serializer"""
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserActivitySerializer(ModelSerializer):
    """User's last activity serializer"""
    username = serializers.StringRelatedField()
    last_login = serializers.CharField(source='username.last_login')

    class Meta:
        model = UserActivity
        fields = ('id', 'username', 'last_login', 'last_request')
