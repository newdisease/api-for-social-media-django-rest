from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostSerializer(ModelSerializer):
    """Post-list & post-detail serializers"""
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ('title', 'body', 'author', 'created_at')
